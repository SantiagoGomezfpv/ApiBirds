import math
import torch
import librosa
import torchaudio
import numpy as np
import pandas as pd
from pathlib import Path
import torchvision.transforms as transforms

class MelSpecComputer:
    def __init__(self, sr, n_mels, fmin=0, fmax=16000, **kwargs):
        self.sr = sr
        self.n_mels = n_mels
        self.fmin = fmin
        self.fmax = fmax
        kwargs["n_fft"] = kwargs.get("n_fft", self.sr//10)
        kwargs["hop_length"] = kwargs.get("hop_length", self.sr//(10*4))
        self.kwargs = kwargs

    def __call__(self, y):
        melspec = librosa.feature.melspectrogram(y=y, sr=self.sr, n_mels=self.n_mels, fmin=self.fmin, fmax=self.fmax, **self.kwargs,)
        melspec = librosa.power_to_db(melspec).astype(np.float32)
        return melspec

def normalize(X, eps=1e-6, mean=None, std=None):
    mean = mean or X.mean()
    std = std or X.std()
    X = (X - mean) / (std + eps)
    _min, _max = X.min(), X.max()
    if (_max - _min) > eps:
        V = np.clip(X, _min, _max)
        V = 255 * (V - _min) / (_max - _min)
        V = V.astype(np.uint8)
    else:
        V = np.zeros_like(X, dtype=np.uint8)
    return V

def mono_to_color(image):        # REPLICA LA IMAGEN 3 VECES IMITANDO RGB
    image = image.astype("float32", copy=False) / 255.0
    image = np.stack([image, image, image])
    return image

def load_audio(record, sr=32000, root=Path("./")):
    waveform, sample_rate = torchaudio.load(root.joinpath(record).with_suffix(".ogg").as_posix(),)
    if sample_rate != sr:
        y = torchaudio.transforms.Resample(sample_rate, sr)(waveform) # PONER FRECUENCIA DE MUESTREO EN 32000 DONDE SEA DIFERENTE
        return y
    else:
        return waveform
sound_len = 5 * 32000          # TAMAÑO DE FRAGMENTACIÓN
do_melspec_1 = MelSpecComputer(sr=32000, n_mels=128)

def load_and_save_test(row):
        sal = torch.tensor([])
        y = load_audio(row, 32000)
        y = y.squeeze()        # QUITAR TAMAÑO "1" 
        len_y = len(y)         # LONGITUD TOTAL DE LA SEÑAL

        for i in range(math.ceil(len(y) / sound_len)):           # NUMERO DE SEGMENTOS 120
            t_min = max(i * sound_len - 32000 , 0)               # TIEMPO MINIMO DEL SEGMENTO
            t_max = min((i + 1) * sound_len + 32000, len_y)      # TIEMPO MAXIMO DEL SEGMENTO
            labl = np.array(y[int(t_min):int(t_max)])            # INTERVALO CON 1 SEGUNDO DE TRASLAPE CON EL ANTERIOR Y EL SIGUIENTE
            if len(labl) < (7 * 32000):
                labl = np.hstack([labl, labl])[:(7 * 32000)]     
            
            transform = transforms.Compose([transforms.Resize((224,224)),])
                        # transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))])
            
            R = transform(torch.from_numpy(mono_to_color(do_melspec_1(labl))).float())
            R = torch.unsqueeze(R,axis=0)
            sal = torch.cat((sal,R),dim=0)
        return sal

@torch.no_grad()
def get_thresh_preds(output, thresh=0.25):
    out = torch.nn.functional.softmax(output, dim=1) #pasar a probabilidades
    o = (-out).argsort(1)
    npreds = (out > thresh).sum(1)
    preds = []
    for oo, npred in zip(o, npreds):
        preds.append(oo[:npred].cpu().numpy().tolist())
    return preds

def get_bird_names(preds):
    bird_names = []
    for pred in preds:
        if not pred:
            bird_names.append("nocall")
        else:
            bird_names.append(" ".join([INV_LABEL_IDS[bird_id] for bird_id in pred]))
    return bird_names

df_train = pd.read_csv(r"./train_metadata.csv")
LABEL_IDS = {label: label_id for label_id,label in enumerate(sorted(df_train["primary_label"].unique()))}
INV_LABEL_IDS = {val: key for key,val in LABEL_IDS.items()}

model = torch.load(r"./ModeloDensenet121.pkl", map_location=torch.device('cpu'))
model.load_state_dict(torch.load(r"./Densenet121Mejorada.pkl", map_location=torch.device('cpu')))
model.eval();

def Modelo(): 
    Audio = r"./AudioModelo.ogg"
    y = load_and_save_test(Audio)
    output = model(y)
    Result = get_bird_names(get_thresh_preds(output))
    prediction = " - ".join(Result)
    return prediction