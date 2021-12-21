import time
from dds import *

start = time.time()
url_performance = 'http://10.193.32.10:8803/gpm/perform.xml'
sysname = 'BDZ3'
nsec = (0, 86400)                                                             #(today, yesterday)
day = time.strftime("%y%m%d", time.localtime(int(time.time())-nsec[0]))       #pick a day
delta = '1600'                                                               #start time('HHMM') of the day
mintime = 60                                                                 #value of M III mintime(erbrmf04)
count = 10                                                              

slots_total = {'BDZ3':1_951_195}

report_class_gtsa = ('RCB','RMQ','RIWEB')
report_class_uat = ('C$CBAA01', 'C$CBAA02', 'C$CBAA03', 'C$CBAA04', 'C$CBAA06', 'C$CBAR01', 'C$CBAR02', 'C$CBAT01')
report_class_dev = ('T$VBAA01', 'T$VBAA02', 'T$VBAA03', 'T$VBAA04', 'T$VBAA06', 'T$VBAR01', 'T$VBAR02', 'T$VBAT01') 
report_class_sit = ('T$IBAA01', 'T$IBAA02', 'T$IBAA03', 'T$IBAA04', 'T$IBAA06', 'T$IBAR01', 'T$IBAR02', 'T$IBAT01')
report_class_prd = ('C$V01A01', 'C$V01A02', 'C$V01A03', 'C$V01A04', 'C$V01A06', 'C$V01R01', 'C$V01R02', 'C$V01T01')
report_class_batch = ('RBATCRIT', 'RBATHIGH', 'RBATLOW', 'RBATNORM', 'RBATPTE')
report_class_stc = ('MQ3ACHIN',)
report_class = report_class_uat + report_class_dev + report_class_sit + report_class_prd + report_class_stc + report_class_batch 
report_class_tran = ('RCOFYD', 'RCOF6Y', 'RCVRSI', 'RCCWXN')
fcs_channels = ('80','81','82','83','84','85','86','87')
matrix_titile = (
                ('INTERVAL' , 'MVS_BSY%' , 'STOR_AVAL%', 'SLOTS_AVAL%' , 'CSA%', 'SQA%', 'ECSA%', 'ESQA%', 'FCS_CHAN_ALL%') + tuple([i+'_APPL%' for i in report_class]) 
                  + tuple([i[2:]+'_TPS' for i in report_class_tran]) + tuple([i[2:]+'_rspTim(ms)' for i in report_class_tran])
                )
filter_hi_100 = 'HI=100'

resource_processor = sysname + ',,PROCESSOR'
id_mvs_utilization_cp = '8D0420'
id_appl_by_report_class = '8D2720'

resource_csa = sysname + ',,CSA'
id_csa_utilization = '8D0530'

resource_sqa = sysname + ',,SQA'
id_sqa_utilization = '8D0530'

resource_ecsa = sysname + ',,ECSA'
id_ecsa_utilization = '8D0530'

resource_esqa = sysname + ',,ESQA'
id_esqa_utilization = '8D0530'

resource_central_storage = sysname + ',,CENTRAL_STORAGE'
id_frames_available = '8D0380'

resource_sysplex = ',PLEX' + sysname + ',SYSPLEX'
id_transaction_ended_rate = '8D3230' 
id_response_time = '8D5F00'

resource_channel = sysname + ',,ALL_CHANNELS'
id_utilization_by_channel = '8D0090'

resource_auxiliary_storage = sysname + ',,AUXILIARY_STORAGE'
id_slots_available = '8D2F10'

interval_sec = int(time.mktime(time.strptime(day+delta, "%y%m%d%H%M")))        # time in seconds since the epoch, of the required start date/time 
matrix ={}                                                                     #dictionary for data

for i in range(count):
        interval_start = time.strftime("%Y%m%d%H%M%S", time.localtime(interval_sec+i*mintime))     #get next interval_start in format "YYMMDDHHMMSS"
        interval_end = time.strftime("%Y%m%d%H%M%S", time.localtime(interval_sec+(i+1)*mintime))   #get next interval_end in format "YYMMDDHHMMSS"

        #mvs busy
        mvs_utilization_cp_parm = {'resource':resource_processor, 'id':id_mvs_utilization_cp, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}
        root = getddsrootv2(url=url_performance, parm=mvs_utilization_cp_parm, use=user, passwd=password)
        if root != None:
                matrix[interval_start] = []
                matrix[interval_start].append(parse_root(root))
        else: break
                
        #%frames available
        frames_available_parm = {'resource':resource_central_storage, 'id':id_frames_available, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=frames_available_parm, use=user, passwd=password)
        matrix[interval_start].append(parse_root(root))

        #%slot available
        slots_available_parm = {'resource':resource_auxiliary_storage, 'id':id_slots_available, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=slots_available_parm, use=user, passwd=password)
        matrix[interval_start].append(str(round(int(parse_root(root))*100/slots_total['BDZ3'],2)))

        #%CSA
        csa_utilization_parm = {'resource':resource_csa, 'id':id_csa_utilization, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=csa_utilization_parm, use=user, passwd=password)
        matrix[interval_start].append(parse_root(root))

        #%SQA
        sqa_utilization_parm = {'resource':resource_sqa, 'id':id_sqa_utilization, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=sqa_utilization_parm, use=user, passwd=password)
        matrix[interval_start].append(parse_root(root))

        #%ECSA
        ecsa_utilization_parm = {'resource':resource_ecsa, 'id':id_ecsa_utilization, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=ecsa_utilization_parm, use=user, passwd=password)
        matrix[interval_start].append(parse_root(root))

        #%ESQA
        esqa_utilization_parm = {'resource':resource_esqa, 'id':id_esqa_utilization, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=esqa_utilization_parm, use=user, passwd=password)
        matrix[interval_start].append(parse_root(root))

        #%ALL_CHANNELS
        fcs_channel_utilization_parm = {'resource':resource_channel, 'id':id_utilization_by_channel, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}        
        root = getddsrootv2(url=url_performance, parm=fcs_channel_utilization_parm, use=user, passwd=password)
        matrix[interval_start].append(average(parse_root_with_iter(fcs_channels,root)))
        
        #appl by wlm report class        
        appl_by_report_class_parm = {'resource':resource_processor, 'id':id_appl_by_report_class, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}
        root = getddsrootv2(url=url_performance, parm=appl_by_report_class_parm, use=user, passwd=password)
        matrix[interval_start].extend(parse_root_with_iter(report_class,root))
                        
        #transaction_ended_rate by report class
        tran_ended_rate_parm = {'resource':resource_sysplex, 'id':id_transaction_ended_rate, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}                
        root = getddsrootv2(url=url_performance, parm=tran_ended_rate_parm, use=user, passwd=password)
        matrix[interval_start].extend(parse_root_with_iter(report_class_tran,root))

        #transaction_response_time by report class
        tran_response_time_parm = {'resource':resource_sysplex, 'id':id_response_time, 'filter':filter_hi_100, 'range':interval_start + ',' + interval_end}                
        root = getddsrootv2(url=url_performance, parm=tran_response_time_parm, use=user, passwd=password)
        matrix[interval_start].extend(parse_root_with_iter(report_class_tran,root))

        print(interval_start, end='\t')


with open('DDS_REPORT_%s.D%s' %(sysname,day),'w') as outfile:
        outfile.write('%-15s' * len(matrix_titile) %(matrix_titile))
        if len(matrix) > 0:  
                for key in matrix.keys():
                        outfile.write('\n' + '%-15s' * len((matrix_titile)) %(key[2:], *(matrix[key])))
        else: outfile.write('\n' + 'data can't be requested')
        stop = time.time()
        message = '\nDDS_REPORT_{s}.D{d} saved in {dur} seconds.'.format(s=sysname,d=day,dur=round(stop-start,1))
        print(message)
        outfile.write(message)
