from datiocr.service.task import DatiOcr
from datetime import datetime

if __name__ == '__main__':
    bucket = "ocrdatidev"
    init = datetime.now()
    # lista = ['IE_000.pdf', 'IE_001.pdf', 'IE_002.pdf', 'IE_003.pdf', 'IE_004.pdf', 'IE_005.pdf', 'IE_006.pdf']
    lista = ['IE_000.pdf']
    for i in lista:
        local_init = datetime.now()
        wc = DatiOcr(bucket, i)
        print(wc.run(), f"TIME LOCAL EXECUTION {datetime.now() - local_init}")
    print(f"###### TIME EXECUTION FOR {len(lista)}-PDFS IS: {datetime.now() - init} ######")

