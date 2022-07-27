# ASTF

This project provides the demo system of ASTF that can depict the time-varying patterns of radio signals to fulfill long-term signal analysis requirements in radio monitoring and management scenarios. 

## Dependencies

This project adopts front-end separation technology, the front-end adopts Vue framework, and the back-end adopts Flask framework. The environments that need to be configured in advance are:

- Python 3.7.7
- Node 14.16.1

Other dependencies can be installed through commands, among which the front-end dependencies need to execute the following commands:

```powershell
cd view
npm install
```

The backend dependencies need to execute the following commands:

```powershell
cd server
pip install -r requirements.txt
```

## Usage

We provide *two simple data* for you to experience ASTF, before which you need to enable front-end and back-end, respectively.

#### 1. Start the front-end service

You can start the front-end service by executing the following command

```powershell
cd view 
npm run serve
```

#### 2. Start back-end service

```powershell
cd server
python app.py
```

#### 3. Open the URL for use.

Open a browser and enter the following url address: http://localhost:8080/

## 参考论文

- Ying Zhao, Luhao Ge, Huixuan Xie, Genghuai Bai, Zhao Zhang, Fangfang Zhou and Yun Lin. ASTF: Visual Abstractions of Time-Varying Patterns in Radio Signals[C].*IEEE* *Visualization* *Conference*,2022.

