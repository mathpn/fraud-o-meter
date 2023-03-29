"""
Inference worker that uses RabbitMQ (pika).
"""

import argparse
import json
import threading
from functools import partial
from typing import Callable

import pandas as pd
from pika import BasicProperties

from app.bridge import create_rabbitmq_client
from app.logger import logger


def callback(
    channel,
    method,
    properties: BasicProperties,
    body: str,
    *,
    worker_id: int,
    inference_fn: Callable,
) -> None:
    transaction_info = json.loads(body)
    result = inference_fn(transaction_info)
    logger.debug(f"inference result (worker {worker_id}): {result}")

    channel.basic_publish(
        exchange="",
        routing_key=properties.reply_to,
        properties=BasicProperties(headers=properties.headers),
        body=result,
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


class ThreadedConsumer(threading.Thread):
    def __init__(
        self,
        worker_id: int,
        rabbitmq_creator: Callable,
        inference_fn: Callable,
    ):
        super().__init__()
        self.worker_id = worker_id
        self.rabbitmq_client, *_ = rabbitmq_creator()
        self.callback = partial(
            callback,
            worker_id=worker_id,
            inference_fn=inference_fn,
        )
        logger.debug(f"consumer worker {worker_id} ready")

    def run(self):
        self.rabbitmq_client.basic_qos(prefetch_count=1)
        self.rabbitmq_client.basic_consume(
            queue="summarizer_inference_queue", on_message_callback=self.callback
        )
        self.rabbitmq_client.start_consuming()
        logger.info(f"consumer worker {self.worker_id} - starting to consume")


def create_inference(model):
    def inference(transaction_info):
        data = pd.DataFrame(index=[0], data=transaction_info)
        # TODO label encoding!
        return model.predict(data)
    return inference


def main():
    import lightgbm as lgbm
    # loading the model
    model = lgbm.Booster(model_file="./models/baseline_lgbm.txt")
    inference = create_inference(model)
    transaction_info = json.loads('{"TransactionID":2987010,"isFraud":0,"TransactionDT":86549,"TransactionAmt":75.887,"ProductCD":"C","card1":16496,"card2":352.0,"card3":117.0,"card4":"mastercard","card5":134.0,"card6":"credit","addr1":null,"addr2":null,"dist1":null,"dist2":null,"P_emaildomain":"gmail.com","R_emaildomain":"gmail.com","C1":1.0,"C2":4.0,"C3":0.0,"C4":1.0,"C5":0.0,"C6":1.0,"C7":1.0,"C8":1.0,"C9":0.0,"C10":1.0,"C11":2.0,"C12":2.0,"C13":2.0,"C14":1.0,"D1":1.0,"D2":1.0,"D3":0.0,"D4":0.0,"D5":0.0,"D6":0.0,"D7":0.0,"D8":83.0,"D9":0.0,"D10":0.0,"D11":null,"D12":0.0,"D13":0.0,"D14":0.0,"D15":0.0,"M1":null,"M2":null,"M3":null,"M4":"M0","M5":null,"M6":null,"M7":null,"M8":null,"M9":null,"V1":null,"V2":null,"V3":null,"V4":null,"V5":null,"V6":null,"V7":null,"V8":null,"V9":null,"V10":null,"V11":null,"V12":0.0,"V13":0.0,"V14":1.0,"V15":1.0,"V16":1.0,"V17":1.0,"V18":1.0,"V19":1.0,"V20":1.0,"V21":1.0,"V22":1.0,"V23":1.0,"V24":1.0,"V25":1.0,"V26":1.0,"V27":0.0,"V28":0.0,"V29":0.0,"V30":0.0,"V31":1.0,"V32":1.0,"V33":1.0,"V34":1.0,"V35":0.0,"V36":0.0,"V37":4.0,"V38":4.0,"V39":1.0,"V40":1.0,"V41":1.0,"V42":1.0,"V43":1.0,"V44":1.0,"V45":1.0,"V46":2.0,"V47":2.0,"V48":0.0,"V49":0.0,"V50":1.0,"V51":2.0,"V52":2.0,"V53":0.0,"V54":0.0,"V55":4.0,"V56":4.0,"V57":1.0,"V58":1.0,"V59":1.0,"V60":1.0,"V61":1.0,"V62":1.0,"V63":1.0,"V64":1.0,"V65":1.0,"V66":2.0,"V67":2.0,"V68":0.0,"V69":0.0,"V70":0.0,"V71":1.0,"V72":1.0,"V73":2.0,"V74":2.0,"V75":0.0,"V76":0.0,"V77":3.0,"V78":3.0,"V79":1.0,"V80":1.0,"V81":1.0,"V82":1.0,"V83":1.0,"V84":1.0,"V85":1.0,"V86":1.0,"V87":1.0,"V88":1.0,"V89":0.0,"V90":0.0,"V91":0.0,"V92":1.0,"V93":1.0,"V94":1.0,"V95":0.0,"V96":0.0,"V97":0.0,"V98":0.0,"V99":0.0,"V100":0.0,"V101":0.0,"V102":0.0,"V103":0.0,"V104":0.0,"V105":0.0,"V106":0.0,"V107":1.0,"V108":1.0,"V109":1.0,"V110":1.0,"V111":1.0,"V112":1.0,"V113":1.0,"V114":1.0,"V115":1.0,"V116":1.0,"V117":1.0,"V118":1.0,"V119":1.0,"V120":1.0,"V121":1.0,"V122":1.0,"V123":1.0,"V124":1.0,"V125":1.0,"V126":0.0,"V127":0.0,"V128":0.0,"V129":0.0,"V130":0.0,"V131":0.0,"V132":0.0,"V133":0.0,"V134":0.0,"V135":0.0,"V136":0.0,"V137":0.0,"V138":null,"V139":null,"V140":null,"V141":null,"V142":null,"V143":null,"V144":null,"V145":null,"V146":null,"V147":null,"V148":null,"V149":null,"V150":null,"V151":null,"V152":null,"V153":null,"V154":null,"V155":null,"V156":null,"V157":null,"V158":null,"V159":null,"V160":null,"V161":null,"V162":null,"V163":null,"V164":null,"V165":null,"V166":null,"V167":3.0,"V168":3.0,"V169":3.0,"V170":4.0,"V171":4.0,"V172":2.0,"V173":1.0,"V174":2.0,"V175":2.0,"V176":4.0,"V177":0.0,"V178":0.0,"V179":0.0,"V180":1.0,"V181":1.0,"V182":1.0,"V183":1.0,"V184":1.0,"V185":1.0,"V186":1.0,"V187":1.0,"V188":1.0,"V189":1.0,"V190":1.0,"V191":1.0,"V192":1.0,"V193":1.0,"V194":1.0,"V195":1.0,"V196":1.0,"V197":1.0,"V198":1.0,"V199":1.0,"V200":1.0,"V201":1.0,"V202":166.2153930664,"V203":166.2153930664,"V204":166.2153930664,"V205":90.3279037476,"V206":31.841299057,"V207":90.3279037476,"V208":90.3279037476,"V209":90.3279037476,"V210":90.3279037476,"V211":0.0,"V212":0.0,"V213":0.0,"V214":75.8874969482,"V215":75.8874969482,"V216":75.8874969482,"V217":3.0,"V218":3.0,"V219":3.0,"V220":3.0,"V221":4.0,"V222":4.0,"V223":2.0,"V224":2.0,"V225":2.0,"V226":0.0,"V227":2.0,"V228":4.0,"V229":4.0,"V230":4.0,"V231":0.0,"V232":0.0,"V233":0.0,"V234":1.0,"V235":1.0,"V236":1.0,"V237":1.0,"V238":1.0,"V239":1.0,"V240":1.0,"V241":1.0,"V242":1.0,"V243":1.0,"V244":1.0,"V245":1.0,"V246":1.0,"V247":1.0,"V248":1.0,"V249":1.0,"V250":1.0,"V251":1.0,"V252":1.0,"V253":1.0,"V254":1.0,"V255":1.0,"V256":1.0,"V257":1.0,"V258":1.0,"V259":1.0,"V260":1.0,"V261":1.0,"V262":1.0,"V263":166.2153930664,"V264":166.2153930664,"V265":166.2153930664,"V266":90.3279037476,"V267":90.3279037476,"V268":90.3279037476,"V269":0.0,"V270":90.3279037476,"V271":90.3279037476,"V272":90.3279037476,"V273":0.0,"V274":0.0,"V275":0.0,"V276":75.8874969482,"V277":75.8874969482,"V278":75.8874969482,"V279":3.0,"V280":3.0,"V281":3.0,"V282":4.0,"V283":4.0,"V284":2.0,"V285":2.0,"V286":1.0,"V287":2.0,"V288":2.0,"V289":2.0,"V290":4.0,"V291":4.0,"V292":4.0,"V293":0.0,"V294":0.0,"V295":0.0,"V296":1.0,"V297":1.0,"V298":1.0,"V299":1.0,"V300":1.0,"V301":1.0,"V302":1.0,"V303":1.0,"V304":1.0,"V305":1.0,"V306":166.2153930664,"V307":166.2153930664,"V308":166.2153930664,"V309":90.3279037476,"V310":90.3279037476,"V311":31.841299057,"V312":90.3279037476,"V313":90.3279037476,"V314":90.3279037476,"V315":90.3279037476,"V316":0.0,"V317":0.0,"V318":0.0,"V319":75.8874969482,"V320":75.8874969482,"V321":75.8874969482,"V322":null,"V323":null,"V324":null,"V325":null,"V326":null,"V327":null,"V328":null,"V329":null,"V330":null,"V331":null,"V332":null,"V333":null,"V334":null,"V335":null,"V336":null,"V337":null,"V338":null,"V339":null,"id_01":-5.0,"id_02":191631.0,"id_03":0.0,"id_04":0.0,"id_05":0.0,"id_06":0.0,"id_07":null,"id_08":null,"id_09":0.0,"id_10":0.0,"id_11":100.0,"id_12":"NotFound","id_13":52.0,"id_14":null,"id_15":"Found","id_16":"Found","id_17":121.0,"id_18":null,"id_19":410.0,"id_20":142.0,"id_21":null,"id_22":null,"id_23":null,"id_24":null,"id_25":null,"id_26":null,"id_27":null,"id_28":"Found","id_29":"Found","id_30":null,"id_31":"chrome 62.0","id_32":null,"id_33":null,"id_34":null,"id_35":"F","id_36":"F","id_37":"T","id_38":"T","DeviceType":"desktop","DeviceInfo":"Windows"}')
    print(inference(transaction_info))


if __name__ == "__main__":
    main()
