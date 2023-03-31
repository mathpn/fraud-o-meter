# fraud-o-meter

## Overview

Credit card fraud detection API using **FastAPI**, **Scikit-Learn** and **RabbitMQ**. Docker-compose is used and there are three services: rabbitmq (of course), the FastAPI app and a consumer worker.

The architecture is very simple and focused on fast response times. The endpoint in the app receives transaction information and adds it to a rabbitmq queue. This queue is then consumed by the consumer (which is threaded for better performance), which adds the result to another queue. The endpoint waits for the inference result and returns it when it is received in the result queue. The endpoint uses asynchronous operations when posible so that other requests can be processed while waiting for inference.

## Dataset

The dataset comes from the [IEEE-CIS Fraud Detection](https://www.kaggle.com/competitions/ieee-fraud-detection/) Kaggle competition. This dataset contains many missing values, therefore we must either impute missing values or use a model that can handle them intervally. Here, the latter was chosen since the best performing model (in my training) was a XGBoost classifier.

## EDA and training

EDA and training are described in the eda_train.ipynb jupyter notebook.

## Endpoint

There's only one endpoint:

- /detect_fraud (POST)

It expects a very large body with many parameters describind the transaction. Variable names are unfortunately not very clear due to anonymity concerns with the dataset.

### Sample request body

```json
{"TransactionDT":847863.0,"TransactionAmt":335.0,"ProductCD":4.0,"card1":13271.0,"card2":385.0,"card3":36.0,"card4":2.0,"card5":106.0,"card6":2.0,"addr1":302.0,"addr2":62.0,"dist1":null,"dist2":null,"P_emaildomain":16.0,"R_emaildomain":60.0,"C1":3.0,"C2":3.0,"C3":0.0,"C4":0.0,"C5":0.0,"C6":1.0,"C7":0.0,"C8":0.0,"C9":2.0,"C10":0.0,"C11":3.0,"C12":0.0,"C13":5.0,"C14":3.0,"D1":40.0,"D2":40.0,"D3":0.0,"D4":257.0,"D5":0.0,"D6":null,"D7":null,"D8":null,"D9":null,"D10":40.0,"D11":null,"D12":null,"D13":null,"D14":null,"D15":40.0,"M1":2.0,"M2":2.0,"M3":2.0,"M4":0.0,"M5":0.0,"M6":0.0,"M7":2.0,"M8":2.0,"M9":2.0,"V1":null,"V2":null,"V3":null,"V4":null,"V5":null,"V6":null,"V7":null,"V8":null,"V9":null,"V10":null,"V11":null,"V12":0.0,"V13":0.0,"V14":1.0,"V15":0.0,"V16":0.0,"V17":0.0,"V18":0.0,"V19":1.0,"V20":1.0,"V21":0.0,"V22":0.0,"V23":1.0,"V24":1.0,"V25":1.0,"V26":1.0,"V27":0.0,"V28":0.0,"V29":0.0,"V30":0.0,"V31":0.0,"V32":0.0,"V33":0.0,"V34":0.0,"V35":1.0,"V36":1.0,"V37":1.0,"V38":1.0,"V39":0.0,"V40":0.0,"V41":1.0,"V42":0.0,"V43":0.0,"V44":1.0,"V45":1.0,"V46":1.0,"V47":1.0,"V48":0.0,"V49":0.0,"V50":0.0,"V51":0.0,"V52":0.0,"V53":0.0,"V54":0.0,"V55":1.0,"V56":1.0,"V57":0.0,"V58":0.0,"V59":0.0,"V60":0.0,"V61":1.0,"V62":1.0,"V63":0.0,"V64":0.0,"V65":1.0,"V66":1.0,"V67":1.0,"V68":0.0,"V69":0.0,"V70":0.0,"V71":0.0,"V72":0.0,"V73":0.0,"V74":0.0,"V75":0.0,"V76":0.0,"V77":1.0,"V78":1.0,"V79":0.0,"V80":0.0,"V81":0.0,"V82":1.0,"V83":1.0,"V84":0.0,"V85":0.0,"V86":1.0,"V87":1.0,"V88":1.0,"V89":0.0,"V90":0.0,"V91":0.0,"V92":0.0,"V93":0.0,"V94":0.0,"V95":2.0,"V96":2.0,"V97":2.0,"V98":1.0,"V99":1.0,"V100":1.0,"V101":1.0,"V102":1.0,"V103":1.0,"V104":0.0,"V105":0.0,"V106":0.0,"V107":1.0,"V108":1.0,"V109":1.0,"V110":1.0,"V111":1.0,"V112":1.0,"V113":1.0,"V114":1.0,"V115":1.0,"V116":1.0,"V117":1.0,"V118":1.0,"V119":1.0,"V120":1.0,"V121":1.0,"V122":1.0,"V123":1.0,"V124":1.0,"V125":1.0,"V126":435.0,"V127":435.0,"V128":435.0,"V129":100.0,"V130":100.0,"V131":100.0,"V132":335.0,"V133":335.0,"V134":335.0,"V135":0.0,"V136":0.0,"V137":0.0,"V138":null,"V139":null,"V140":null,"V141":null,"V142":null,"V143":null,"V144":null,"V145":null,"V146":null,"V147":null,"V148":null,"V149":null,"V150":null,"V151":null,"V152":null,"V153":null,"V154":null,"V155":null,"V156":null,"V157":null,"V158":null,"V159":null,"V160":null,"V161":null,"V162":null,"V163":null,"V164":null,"V165":null,"V166":null,"V167":null,"V168":null,"V169":null,"V170":null,"V171":null,"V172":null,"V173":null,"V174":null,"V175":null,"V176":null,"V177":null,"V178":null,"V179":null,"V180":null,"V181":null,"V182":null,"V183":null,"V184":null,"V185":null,"V186":null,"V187":null,"V188":null,"V189":null,"V190":null,"V191":null,"V192":null,"V193":null,"V194":null,"V195":null,"V196":null,"V197":null,"V198":null,"V199":null,"V200":null,"V201":null,"V202":null,"V203":null,"V204":null,"V205":null,"V206":null,"V207":null,"V208":null,"V209":null,"V210":null,"V211":null,"V212":null,"V213":null,"V214":null,"V215":null,"V216":null,"V217":null,"V218":null,"V219":null,"V220":null,"V221":null,"V222":null,"V223":null,"V224":null,"V225":null,"V226":null,"V227":null,"V228":null,"V229":null,"V230":null,"V231":null,"V232":null,"V233":null,"V234":null,"V235":null,"V236":null,"V237":null,"V238":null,"V239":null,"V240":null,"V241":null,"V242":null,"V243":null,"V244":null,"V245":null,"V246":null,"V247":null,"V248":null,"V249":null,"V250":null,"V251":null,"V252":null,"V253":null,"V254":null,"V255":null,"V256":null,"V257":null,"V258":null,"V259":null,"V260":null,"V261":null,"V262":null,"V263":null,"V264":null,"V265":null,"V266":null,"V267":null,"V268":null,"V269":null,"V270":null,"V271":null,"V272":null,"V273":null,"V274":null,"V275":null,"V276":null,"V277":null,"V278":null,"V279":2.0,"V280":2.0,"V281":2.0,"V282":3.0,"V283":3.0,"V284":1.0,"V285":1.0,"V286":0.0,"V287":1.0,"V288":2.0,"V289":2.0,"V290":1.0,"V291":1.0,"V292":1.0,"V293":1.0,"V294":1.0,"V295":1.0,"V296":0.0,"V297":0.0,"V298":0.0,"V299":0.0,"V300":0.0,"V301":0.0,"V302":0.0,"V303":0.0,"V304":0.0,"V305":1.0,"V306":435.0,"V307":435.0,"V308":435.0,"V309":100.0,"V310":100.0,"V311":0.0,"V312":100.0,"V313":195.5,"V314":195.5,"V315":195.5,"V316":335.0,"V317":335.0,"V318":335.0,"V319":0.0,"V320":0.0,"V321":0.0,"V322":null,"V323":null,"V324":null,"V325":null,"V326":null,"V327":null,"V328":null,"V329":null,"V330":null,"V331":null,"V332":null,"V333":null,"V334":null,"V335":null,"V336":null,"V337":null,"V338":null,"V339":null,"id_01":null,"id_02":null,"id_03":null,"id_04":null,"id_05":null,"id_06":null,"id_07":null,"id_08":null,"id_09":null,"id_10":null,"id_11":null,"id_12":2.0,"id_13":54.0,"id_14":25.0,"id_15":3.0,"id_16":2.0,"id_17":104.0,"id_18":18.0,"id_19":522.0,"id_20":394.0,"id_21":490.0,"id_22":25.0,"id_23":3.0,"id_24":12.0,"id_25":341.0,"id_26":95.0,"id_27":2.0,"id_28":2.0,"id_29":2.0,"id_30":75.0,"id_31":130.0,"id_32":4.0,"id_33":260.0,"id_34":4.0,"id_35":2.0,"id_36":2.0,"id_37":2.0,"id_38":2.0,"DeviceType":2.0,"DeviceInfo":1786.0}
```

The endpoint returns the fraud probability (range 0-1) for the provided transaction:

```json
{
  "fraud_probability": 0.12974974326354488
}
```
