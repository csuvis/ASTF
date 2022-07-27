# ASTF

This project is named with ASTF, Abstracted Signal Time-Frequency Diagram. ASTF is a newly designed visualization diagram that can depict the long-term (i.e., hours, 1-2 days, and even 1-2 weeks) time-varying patterns of radio signals to fulfill long-term signal analysis requirements in radio monitoring and management scenarios. 

## Dependencies

This project adopts a front-back separation technology. The front-end adopts a Vue framework and the back-end adopts a Flask framework. The running environments include:

- Python 3.7.7
- Node 14.16.1

Other dependencies can be installed through commands. Specifically, the front-end dependencies need to execute the following commands:

```powershell
cd view
npm install
```

The back-end dependencies need to execute the following commands:

```powershell
cd server
pip install -r requirements.txt
```

## Usage

We provide *two simple datasets*  for testing.

#### 1. Start the front-end service

You can start the front-end service by executing the following commands:

```powershell
cd view 
npm run serve
```

#### 2. Start the back-end service 

You can start the back-end service by executing the following commands:

```powershell
cd server
python app.py
```

#### 3. Open the URL

Open a browser and enter the following URL address: http://localhost:8080/

## Reference Paper

- Ying Zhao, Luhao Ge, Huixuan Xie, Genghuai Bai, Zhao Zhang, et al. ASTF: Visual Abstractions of Time-Varying Patterns in Radio Signals. Accepted by *IEEE* *VIS* 2022 and *IEEE Transactions on Visualization and Computer Graphics*.

