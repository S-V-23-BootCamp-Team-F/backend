## 모델 평가 진행
import torch
from torch import nn
import torchvision.transforms as transforms
import torch.nn.functional as F
import PIL
import os, urllib

# 입력 데이터 데이터 경로 지정

def ai(image_path, model_path) :
    class Dataset(torch.utils.data.Dataset):
        def __init__(self, transform):
            super(Dataset, self).__init__()
            self.transform = transform
            self.image_list = []

            image = urllib.request.urlopen(image_path)
            self.image_list.append(image)
            
        def __len__(self):
            return len(self.image_list)

        def __getitem__(self, index):
            img = PIL.Image.open(self.image_list[index])
            img = img.convert('RGB')
            img = self.transform(img)
            return img

    # 입력 데이터 전처리 진행
    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    test_dataset = Dataset(transform=test_transform)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=False, num_workers=0)


    device = "cpu"
    # 모델 경로 지정헤주기
    model = torch.load(model_path, map_location=device)

    model.eval()

    pred = ''
    with torch.no_grad():
        for x in test_loader:
            x = x.to(device)
            out=model(x)
            pred_idx = torch.argmax(F.softmax(out, dim=1), dim=1)
            pred = pred_idx
            
    predict = pred.detach().cpu().numpy()
    return predict.item()

# ai("./plants/inference/workspace/1.png", "./plants/inference/model.pt")
#bel_map_rev = {0: '일소피해', 1: '정상', 2: '축과병', 3: '포도노균병', 4: '포도노균병반응', 5: '포도탄저병', 6: '포도탄저병반응'}