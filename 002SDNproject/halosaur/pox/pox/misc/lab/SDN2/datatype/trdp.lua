-- File Name    : trdp.lua
--
-- Copyright    : Zhuzhou CSR Times Electric Co.,Ltd. All Rights Reserved.
--
-- Create Date  : 2013/1/14
--
-- Description  : TRDP process data and message data for wireshark using Lua 5.1
--
-- REV1.0.0     : lisy   2013/1/14  File Create  satisfy the IPT-COM
-- REV2.0.0     : lisy   2013/11/7  File Modified satisfy IEC61375-2-3 standard defined
--
do
--
--
    local pd_port = 17224
	local md_port = 17225
--  process data of TRDP
    local trdp_pd_proto = Proto("TRDP-PD","Train Real-time Data Protocol:Process Data")
    
    local f_pd_sequence = ProtoField.uint32("pd.seq", "Sequence Counter", base.DEC)
    local f_pd_proVer = ProtoField.string("pd.ver", "Protocol Version")
    local f_pd_type_string = ProtoField.string("pd.type", "Type")
	local f_pd_comId = ProtoField.uint32("pd.comid", "Com ID", base.DEC)
    local f_pd_etbTopoCnt = ProtoField.uint32("pd.etbTopo", "etbTopoCount", base.HEX) 
	local f_pd_opTrnTopoCnt = ProtoField.uint32("pd.opTrnTopo", "opTrnTopoCount", base.HEX) 
    local f_pd_datasetLength = ProtoField.uint32("pd.datalen", "Dataset Length", base.DEC)
    local f_pd_reserved = ProtoField.uint32("pd.resv", "Reserved", base.HEX)
    local f_pd_replyComId = ProtoField.uint32("pd.replycomid", "Reply Com ID", base.DEC)
    local f_pd_replyAddress = ProtoField.string("pd.replyip", "Reply IP Address")
    local f_pd_headFCS = ProtoField.uint32("pd.hdfcs", "Header FCS", base.HEX)
    local f_pd_dataset_data = ProtoField.string("pd.data", "Data")
	
--  ETB_CTRL comId=1
    local f_version 	=	ProtoField.string("pd1.version", "version")
    local f_mainVersion	=	ProtoField.uint8("pd1.mainVersion", "Main Version", base.DEC)
    local f_subVersion	=	ProtoField.uint8("pd1.subVersion", "Sub Version", base.DEC)
    local f_reserved1	=	ProtoField.uint16("pd1.reserved1", "Reserved01", base.DEC)
    local f_trnCstNo	=	ProtoField.uint8("pd1.trnCstNo", "Train Consist Number", base.DEC)
    local f_reserved2    = ProtoField.uint8("pd1.reserved2", "Reserved02", base.DEC)
    local f_ownOpCstNo	=	ProtoField.uint8("pd1.ownOpCstNo", "Own OpTrain Consist Number", base.DEC)
    local f_reserved3	=	ProtoField.uint8("pd1.reserved3", "Reserved03", base.DEC)
    local f_cstTopoCnt	=	ProtoField.uint32("pd1.cstTopoCnt", "Consist TopoCnt", base.HEX)
    local f_trnTopoCnt	=	ProtoField.uint32("pd1.trnTopoCnt", "Train TopoCnt", base.HEX)
    local f_opTrnTopoCnt	=	ProtoField.uint32("pd1.opTrnTopoCnt", "Operational Train TopoCnt", base.HEX)
    local f_wasLead	=	ProtoField.uint8("pd1.wasLead", "wasLead", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_reqLead	=	ProtoField.uint8("pd1.reqLead", "reqLead", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_reqLeadDir	=	ProtoField.uint8("pd1.reqLeadDir", "reqLeadDir", base.HEX,{[0x01] = "consist direction 1",[0x02] = "consist direction 2"})
    local f_accLead	=	ProtoField.uint8("pd1.accLead", "accLead", base.HEX,{[0x01] = "false,not accepted",[0x02] = "true,accepted"})
    local f_isLead	=	ProtoField.uint8("pd1.isLead", "isLead", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_clearConfComp	=	ProtoField.uint8("pd1.clearConfComp", "clearConfComp", base.HEX,{[0x01] = "false",[0x02] = "true"})
	local f_corrRequest	=	ProtoField.uint8("pd1.corrRequest", "corrRequest", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_corrInfoSet	=	ProtoField.uint8("pd1.corrInfoSet", "corrInfoSet", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_compStored = ProtoField.uint8("pd1.compStored", "compStored", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_sleepRequest	=	ProtoField.uint8("pd1.sleepRequest", "sleepRequest", base.HEX,{[0x01] = "false",[0x02] = "true"})
    local f_leadVehOfCst	=	ProtoField.uint8("pd1.leadVehOfCst", "leadVehOfCst", base.DEC)
    local f_reserved4	=	ProtoField.uint8("pd1.reserved4", "reserved4", base.DEC)
    local f_reserved5	=	ProtoField.uint16("pd1.reserved5", "reserved5", base.DEC)
    local f_reserved6	=	ProtoField.uint8("pd1.reserved6", "reserved6", base.DEC)

    local f_confVehCnt	=	ProtoField.uint8("pd1.confVehCnt", "Confirm Vehicle Count", base.DEC)
    local f_confVehList	=	ProtoField.string("pd1.confVehList", "Confirm Vehicle")
    local f_confTrnVehNo	=	ProtoField.uint8("pd1.confTrnVehNo", "Confirm Train Vehicle Number", base.DEC)
    local f_confIsLead	=	ProtoField.uint8("pd1.confIsLead", "Confirm IsLead", base.DEC)
    local f_confLeadDir	=	ProtoField.uint8("pd1.confLeadDir", "Confirm LeadDir", base.DEC,{[0]="not relevant",[1]="leading direction 1",[2]="leading direction 2"})
    local f_confVehOrient	=	ProtoField.uint8("pd1.confVehOrient", "confVehOrient", base.DEC,{[0]="not known",[1]="same as operational train direction",
    												[2]="inverse to operational train direction"})
    local f_safetyTrail	=	ProtoField.string("pd1.safetyTrail", "safetyTrail")
    local f_safetyTrailReserved1	=	ProtoField.uint32("pd1.safetyTrailReserved1", "safetyTrailReserved1", base.DEC)
    local f_safetyTrailReserved2	=	ProtoField.uint16("pd1.safetyTrailReserved2", "safetyTrailReserved2", base.DEC)
    local f_safetyTrailVersion	=	ProtoField.string("pd1.safetyTrailVersion", "safetyTrailVersion")
    local f_safetyTrailMainVersion	=	ProtoField.uint8("pd1.safetyTrailMainVersion", "safetyTrailMainVersion", base.DEC)
    local f_safetyTrailSubVersion	=	ProtoField.uint8("pd1.safetyTrailSubVersion", "safetyTrailSubVersion", base.DEC)
    local f_safeSequCount	=	ProtoField.uint32("pd1.safeSequCount", "safeSequCount", base.DEC)
    local f_safetyCode	=	ProtoField.uint32("pd1.safetyCode", "safetyCode", base.DEC)

  
    trdp_pd_proto.fields={f_pd_sequence, f_pd_proVer, f_pd_type_string, f_pd_comId, f_pd_etbTopoCnt, f_pd_opTrnTopoCnt,
                        f_pd_datasetLength, f_pd_reserved, f_pd_replyComId, f_pd_replyAddress, f_pd_headFCS, 
                        f_pd_dataset_data, f_version,f_mainVersion, f_subVersion,f_reserved1,
                        f_trnCstNo, f_reserved2, f_ownOpCstNo, f_reserved3, f_cstTopoCnt, f_trnTopoCnt, f_opTrnTopoCnt,
                        f_wasLead, f_reqLead, f_reqLeadDir, f_accLead, f_isLead, f_clearConfComp, f_corrRequest, f_corrInfoSet,
                        f_compStored, f_sleepRequest, f_leadVehOfCst, f_reserved4, f_reserved5, f_reserved6, f_confVehCnt, f_confVehList,
                        f_confTrnVehNo, f_confIsLead, f_confLeadDir, f_confVehOrient,
                        f_safetyTrail, f_safetyTrailReserved1, f_safetyTrailReserved2,
                        f_safetyTrailVersion, f_safetyTrailMainVersion, f_safetyTrailSubVersion, f_safeSequCount,f_safetyCode} 

    function trdp_pd_proto.dissector(buf,pkt,root)
        local buffer_len = buf:len()
        if buffer_len >= 40 then
            local data_type = buf(6,2):uint()
            if data_type ~= 0x5064 and data_type ~= 0x5072 and data_type ~= 0x5070 then
                pkt.cols.info:set("udp port "..string.format("%05d",pd_port).." conflict with the TRDP-PD protocol")
                return
            end     
            local pd_headLen = 40
            pkt.cols.protocol:set("TRDP-PD")
            pkt.cols.info:set("The Process Data of TRDP")
            local pdTree = root:add(trdp_pd_proto, buf(0, pd_headLen), "TRDP Process Data Header")
            pdTree:append_text("(40 bytes)")
--        	(1)Sequence Counter
			pd_offset = 0
			pdTree:add(f_pd_sequence, buf(pd_offset, 4))
			
--          (2)Protocol Version
			pd_offset = pd_offset + 4
			local pd_version = buf(pd_offset, 2):uint()
			local temp_version = pd_version
			x1 = (temp_version - (temp_version % (16 ^ 2)))
			v1 = x1 / (16 ^ 2)
			v2 = temp_version % (16 ^ 2)
			label = string.format("%0#6x",pd_version)
			label2 = v1.."."..v2.." ("..label..")"
			pdTree:add(f_pd_proVer, buf(pd_offset, 2), label2)
		  
--          (3)Type
			pd_offset = pd_offset + 2
			local pd_type = buf(pd_offset, 2):uint()
			pdTree:add(f_pd_type_string, buf(pd_offset, 2), "Pd".." ("..string.format("%0#6x",pd_type)..")") 

--          (4)Com ID
			pd_offset = pd_offset + 2
			pdTree:add(f_pd_comId, buf(pd_offset, 4))
			pd_comId = buf(pd_offset, 4):uint()
										  			
--          (5)etbTopo Counter
			pd_offset = pd_offset + 4
			pdTree:add(f_pd_etbTopoCnt, buf(pd_offset, 4))
					
--          (6)opTrnTopo Counter
			pd_offset = pd_offset + 4
			pdTree:add(f_pd_opTrnTopoCnt, buf(pd_offset, 4))			
					
--          (7)Dataset Length
			pd_offset = pd_offset + 4
			pdTree:add(f_pd_datasetLength, buf(pd_offset, 4))
	
--          (8)Reserved
			pd_offset = pd_offset + 4
			pdTree:add(f_pd_reserved, buf(pd_offset, 4))
			
--          (9)Reply ComId
			pd_offset = pd_offset + 4
			pdTree:add(f_pd_replyComId, buf(pd_offset, 4))

--          (10Reply Address
			pd_offset = pd_offset + 4
		       local pd_ip = buf(pd_offset, 4):uint()
			local temp_ip = pd_ip
			x1 = (temp_ip - (temp_ip % (16 ^ 6)))
			v1 = x1 / (16 ^ 6)
			temp_ip = temp_ip - x1
			x2 = (temp_ip - (temp_ip % (16 ^ 4)))
			v2 = x2 / (16 ^ 4)
			temp_ip = temp_ip - x2
			x3 = (temp_ip - (temp_ip % (16 ^ 2)))
			v3 = x3 / (16 ^ 2)
			v4 = temp_ip % (16 ^ 2)
			label = string.format("%0#10x",pd_ip)
			label2 = v1.."."..v2.."."..v3.."."..v4.." ("..label..")"
			pdTree:add(f_pd_replyAddress, buf(pd_offset, 4), label2)
			
--     		(11Head FCS
			pd_offset = pd_offset + 4
			pdTree:add(f_pd_headFCS, buf(pd_offset, 4))
	
--          (12Dataset        
			local data_len = buf:len() - 40
			pd_offset = pd_offset + 4
			local datasetTree = root:add(trdp_pd_proto, buf(40, data_len), "TRDP Process Data Dataset")
			datasetTree:append_text(" ("..data_len.." bytes)")
--ETBCTRL COMID=1
			if pd_comId == 1 then
			    local etbctrl = datasetTree:add(trdp_pd_proto, buf(40, data_len), "ETBCTRL telegram")
--version       
			    local version = etbctrl:add(f_version,buf(pd_offset,2), "")
			    version:add(f_mainVersion,buf(pd_offset,1))
			    pd_offset = pd_offset + 1
			    version:add(f_subVersion,buf(pd_offset,1))
--reserved1     
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reserved1,buf(pd_offset,2))
--trnCstNo      
			    pd_offset = pd_offset + 2
			    etbctrl:add(f_trnCstNo,buf(pd_offset,1))
--reserved2     
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reserved2,buf(pd_offset,1))
--ownOpCstNo    
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_ownOpCstNo,buf(pd_offset,1))
--reserved3     
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reserved3,buf(pd_offset,1))
--cstTopoCnt    
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_cstTopoCnt,buf(pd_offset,4))
--trnTopoCnt    
			    pd_offset = pd_offset + 4
			    etbctrl:add(f_trnTopoCnt,buf(pd_offset,4))
--opTrnTopoCnt
			    pd_offset = pd_offset + 4
			    etbctrl:add(f_opTrnTopoCnt,buf(pd_offset,4))
--wasLead       
			    pd_offset = pd_offset + 4
			    etbctrl:add(f_wasLead,buf(pd_offset,1))
--reqLead       
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reqLead,buf(pd_offset,1))
--reqLeadDir    
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reqLeadDir,buf(pd_offset,1))
--accLead       
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_accLead,buf(pd_offset,1))
--isLead        
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_isLead,buf(pd_offset,1))
--clearConfComp
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_clearConfComp,buf(pd_offset,1))
--corrRequest
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_corrRequest,buf(pd_offset,1))
--corrInfoSet
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_corrInfoSet,buf(pd_offset,1))
--compStored    
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_compStored,buf(pd_offset,1))
--sleepRequest
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_sleepRequest,buf(pd_offset,1))
--leadVehOfCst
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_leadVehOfCst,buf(pd_offset,1))
--reserved4     
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reserved4,buf(pd_offset,1))
--reserved5     
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_reserved5,buf(pd_offset,2))
--reserved6     
		        pd_offset = pd_offset + 2
			    etbctrl:add(f_reserved6,buf(pd_offset,1))
--confVehCnt    
			    pd_offset = pd_offset + 1
			    etbctrl:add(f_confVehCnt,buf(pd_offset,1))
			    confVehCnt = buf(pd_offset,1):uint()
--confVehList
				if confVehCnt == 0 then
				etbctrl:add(f_confVehList,buf(pd_offset,0), string.format("None"))
				elseif confVehCnt > 0 then
					for i = 1,confVehCnt do
						local confVehList = etbctrl:add(f_confVehList,buf(pd_offset,4), string.format("List[%d]", i))
						confVehList:add(f_confTrnVehNo,buf(pd_offset,1))
						pd_offset = pd_offset + 1
						confVehList:add(f_confIsLead,buf(pd_offset,1))
						pd_offset = pd_offset + 1
						confVehList:add(f_confLeadDir,buf(pd_offset,1))
						pd_offset = pd_offset + 1
						confVehList:add(f_confVehOrient,buf(pd_offset,1))
						pd_offset = pd_offset + 1
					end
				end
--safetyTrail
				pd_offset = pd_offset + 1
				local safetyTrail = etbctrl:add(f_safetyTrail,buf(pd_offset,16), "")
				safetyTrail:add(f_safetyTrailReserved1,buf(pd_offset,4))
				pd_offset = pd_offset + 4
				safetyTrail:add(f_safetyTrailReserved2,buf(pd_offset,2))
				pd_offset = pd_offset + 2
				local safetyTrailVersion = safetyTrail:add(f_safetyTrailVersion,buf(pd_offset,2))
				safetyTrailVersion:add(f_safetyTrailMainVersion,buf(pd_offset,1))
				pd_offset = pd_offset + 1
				safetyTrailVersion:add(f_safetyTrailSubVersion,buf(pd_offset,1))
				pd_offset = pd_offset + 1
				safetyTrail:add(f_safeSequCount,buf(pd_offset,4))
				pd_offset = pd_offset + 4
				safetyTrail:add(f_safetyCode,buf(pd_offset,4))
			end
        else
        pkt.cols.info:set("udp port "..string.format("%05d",pd_port).." conflict with the TRDP-PD protocol")
        return 
	    end        
    end
  
--
--
--  message data of TRDP  
  
    local trdp_md_proto = Proto("TRDP-MD","Train Real-time Data Protocol:Message Data")
   
	local f_md_sequenceCounter = ProtoField.uint32("md.seq","Sequence Counter",base.DEC)
	local f_md_proVer = ProtoField.string("md.ver", "Protocol Version")
	local f_md_type = ProtoField.string("md.type", "Type")
	local f_md_comId = ProtoField.uint32("md.comid", "Com ID", base.DEC)
	local f_md_etbTopoCnt = ProtoField.uint32("md.etbTopo", "etbTopoCount", base.HEX)
	local f_md_opTrnTopoCnt = ProtoField.uint32("md.opTrnTopo", "opTrnTopoCount", base.HEX)
	local f_md_datasetLength = ProtoField.uint32("md.datalen", "Dataset Length", base.DEC)
	local f_md_replyStatus = ProtoField.uint32("md.stus", "Reply Status", base.HEX)
	local f_md_sessionId = ProtoField.guid("md.seid", "Session ID")
	local f_md_replyTimeout = ProtoField.uint32("md.timeout", "Reply Timeout", base.DEC)
	local f_md_sourceURI = ProtoField.string("md.srcuri", "Source URI")
	local f_md_destURI = ProtoField.string("md.dsturi", "Destination URI")
	local f_md_headFCS = ProtoField.uint32("md.hdfcs", "Header FCS", base.HEX)
	local f_md_dataset_data = ProtoField.string("md.data", "Data")
	
--  CST_INFO comId=2
    local f_version   =    ProtoField.string("md2.version", "Version")
    local f_mainVersion   =    ProtoField.uint8("md2.mainVersion", "Main Version", base.DEC)
    local f_subVersion   =    ProtoField.uint8("md2.subVersion", "Sub Version", base.DEC)
    local f_cstClass		=    ProtoField.uint8("md2.cstClass", "Consist Class", base.DEC)
    local f_reserved1  =   ProtoField.uint8("md2.reserved1", "Reserved01", base.DEC)
    local f_cstId		=		ProtoField.string("md2.cstId", "Consist Id")
    local f_cstType  = 	ProtoField.string("md2.cstType", "Consist Type")
    local f_cstOwner  =		ProtoField.string("md2.cstOwner", "Consist Owner")
    local f_cstUUID		=		ProtoField.string("md2.cstUUID", "Consist UUID")
    local f_reserved2 	=		ProtoField.uint32("md2.reserved2", "Reserved02", base.DEC)
    local f_cstProp		=		ProtoField.string("md2.cstProp", "Consist Properties")
    local f_cstPropMainVersion	=		ProtoField.uint8("md2.cstPropMainVersion", "Consist Property Main Version", base.DEC)
    local f_cstPropSubVersion		=		ProtoField.uint8("md2.cstPropSubVersion", "Consist Property Sub Version", base.DEC)
    local f_cstPropLen		=		ProtoField.uint16("md2.cstPropLen", "Consist Property Length", base.DEC)
    local f_cstPropProp		=		ProtoField.string("md2.cstPropProp", "Consist Property")
   	local f_reserved3		=		ProtoField.uint16("md2.reserved3", "Reserved03", base.DEC)
   	local f_etbCnt		=		ProtoField.uint16("md2.etbCnt", "ETB Count", base.DEC)
   	local f_etbInfoList		=		ProtoField.string("md2.etbInfoList", "ETB Info")
  	local f_etbId		=		ProtoField.uint8("md2.etbId", "ETB Id", base.DEC)
  	local f_cnCnt		=		ProtoField.uint8("md2.cnCnt", "cnCnt", base.DEC)
  	local f_etbInfoReserved1	=		ProtoField.uint16("md2.etbInfoReserved1", "ETB Info Reserved01", base.DEC)
  	local f_reserved4		=		ProtoField.uint16("md2.reserved4", "Reserved04", base.DEC)
  	local f_vehCnt		=		ProtoField.uint16("md2.vehCnt", "Vehicle Count", base.DEC)
  	local f_vehInfoList		=		ProtoField.string("md2.vehInfoList", "Vehicle Info")
  	local f_vehId		=		ProtoField.string("md2.vehId", "Vehicle ID")
  	local f_vehType		=		ProtoField.string("md2.vehType", "Vehicle Type")
  	local f_vehOrient		=		ProtoField.uint8("md2.vehOrient", "Vehicle Orient", base.DEC)
  	local f_cstVehNo	=		ProtoField.uint8("md2.cstVehNo", "Consist Vehicle Number", base.DEC)
  	local f_tractVeh		=		ProtoField.uint8("md2.tractVeh", "Tract Vehicle", base.HEX)
  	local f_vehReserved1	=	ProtoField.uint8("md2.vehReserved1", "Vehicle Reserved01", base.DEC)
  	local f_vehProp		=		ProtoField.string("md2.vehProp", "Vehicle Properties")
  	local f_vehPropMainVersion		=		ProtoField.uint8("md2.vehPropMainVersion", "Vehicle Property Main Version", base.DEC)
  	local f_vehPropSubVersion		=		ProtoField.uint8("md2.vehPropSubVersion", "Vehicle Property Sub Version", base.DEC)
  	local f_vehPropLen		=		ProtoField.uint16("md2.vehPropLen", "Vehicle Property Length", base.DEC)
  	local f_vehPropProp		=		ProtoField.string("md2.vehPropProp", "Vehicle Property")
  	local f_reserved5		=		ProtoField.uint16("md2.reserved5", "Reserved05", base.DEC)
  	local f_fctCnt		=		ProtoField.uint16("md2.fctCnt", "Function Count", base.DEC)
  	local f_fctInfoList		=		ProtoField.string("md2.fctInfoList", "Function Info")
  	local f_fctName		=		ProtoField.string("md2.fctName", "Function Name")
  	local f_fctId		=		ProtoField.uint16("md2.fctId", "Function Id", base.HEX)
  	local f_grp		=		ProtoField.uint8("md2.grp", "Is Group", base.DEC)
  	local f_fctReserved1		=		ProtoField.uint8("md2.fctReserved1", "Function Reserved01", base.DEC)
  	local f_fctCstVehNo		=		ProtoField.uint8("md2.fctCstVehNo", "Function Consist Vehicle Number", base.DEC)
  	local f_fctEtbId		=		ProtoField.uint8("md2.fctEtbId", "Function ETB Id", base.DEC)
  	local f_fctCnId		=		ProtoField.uint8("md2.fctCnId", "Function Consist Id", base.DEC)
  	local f_fctReserved2	=		ProtoField.uint8("md2.fctReserved2", "Function Reserved02", base.DEC)
  	local f_fctProp		=		ProtoField.string("md2.fctProp", "Function Properties")
  	local f_fctPropMainVersion	=		ProtoField.uint8("md2.fctPropMainVersion", "Function Property Main Version", base.DEC)
  	local f_fctPropSubVersion		=		ProtoField.uint8("md2.fctPropSubVersion", "Function Property Sub Version", base.DEC)
  	local f_fctPropLen		=		ProtoField.uint16("md2.fctPropLen", "Function Property Length", base.DEC)
  	local f_fctPropProp		=		ProtoField.string("md2.fctPropProp", "Function Properties")
  	local f_reserved6		=		ProtoField.uint16("md2.reserved6", "Reserved06", base.DEC)
  	local f_cltrCstCnt		=		ProtoField.uint16("md2.cltrCstCnt", "Close Train Consist Count", base.DEC)
  	local f_cltrCstInfoList		=		ProtoField.string("md2.cltrCstInfoList", "Close Train Consist Info")
  	local f_cltrCstUUID		=		ProtoField.string("md2.cltrCstUUID", "Close Train Consist UUID")
  	local f_cltrCstOrient		=		ProtoField.uint8("md2.cltrCstOrient", "Close Train Consist Orient", base.DEC)
  	local f_cltrCstNo		=		ProtoField.uint8("md2.cltrCstNo", "Close Train Consist Number", base.DEC)
  	local f_cltrCstReserved1	=		ProtoField.uint16("md2.cltrCstReserved1", "Close Train Consist Reserved01", base.DEC)
  	local f_cstTopoCnt		=		ProtoField.uint32("md2.cstTopoCnt", "Consist TopoCnt", base.HEX)
--  CSTINFOCTRL comId=3  	
    local f_version3 	=	ProtoField.string("md3.version", "version")
    local f_mainVersion3	=	ProtoField.uint8("md3.mainVersion", "Main Version", base.DEC)
    local f_subVersion3	=	ProtoField.uint8("md3.subVersion", "Sub Version", base.DEC)
	local f_trnCstNo	=	ProtoField.uint8("md3.trnCstNo", "Train Consist Number", base.DEC)
	local f_cstCnt	=	ProtoField.uint8("md3.cstCnt", "Consist Count", base.DEC)
	local f_cstList		=		ProtoField.string("md3.cstList", "Consist List")
	local f_cstUUID		=		ProtoField.string("md3.cstUUID", "Consist UUID")
	local f_cstListCstTopoCnt		=		ProtoField.uint32("md3.cstTopoCnt", "Consist TopoCnt", base.HEX)
	local f_cstListTrnCstNo	=	ProtoField.uint8("md3.trnCstNo", "Train Consist Number", base.DEC)
	local f_cstOrient	=	ProtoField.uint8("md3.cstOrient", "Consist Orientation", base.DEC,{[0x01]="same as train reference direction",
	                                                          [0x02]="inverse as train reference direction"})
	local f_cstReserved1	=	ProtoField.uint16("md3.cstReserved", "Reserved01", base.DEC)   
	local f_trnTopoCnt	=	ProtoField.uint32("md3.trnTopoCnt", "Train TopoCnt", base.HEX)

	local f_safetyTrail	=	ProtoField.string("md3.safetyTrail", "safetyTrail")
    local f_safetyTrailReserved1	=	ProtoField.uint32("md3.safetyTrailReserved1", "safetyTrailReserved1", base.DEC)
    local f_safetyTrailReserved2	=	ProtoField.uint16("md3.safetyTrailReserved2", "safetyTrailReserved2", base.DEC)
    local f_safetyTrailVersion      =	ProtoField.string("md3.safetyTrailVersion", "safetyTrailVersion")
    local f_safetyTrailMainVersion	=	ProtoField.uint8("md3.safetyTrailMainVersion", "safetyTrailMainVersion", base.DEC)
    local f_safetyTrailSubVersion	=	ProtoField.uint8("md3.safetyTrailSubVersion", "safetyTrailSubVersion", base.DEC)
    local f_safeSequCount	=	ProtoField.uint32("md3.safeSequCount", "safeSequCount", base.DEC)
    local f_safetyCode	=	ProtoField.uint32("md3.safetyCode", "safetyCode", base.DEC)
    trdp_md_proto.fields={f_md_sequenceCounter, f_md_proVer, f_md_type, f_md_comId, f_md_etbTopoCnt, f_md_opTrnTopoCnt,
                      f_md_datasetLength, f_md_replyStatus, f_md_sessionId, f_md_replyTimeout, f_md_sourceURI, 
                      f_md_destURI, f_md_headFCS, f_md_dataset_data, f_version,f_mainVersion,
                      f_subVersion, f_cstClass, f_reserved1, f_cstId, f_cstType, f_cstOwner, f_cstUUID, f_reserved2, f_cstProp,
                      f_cstPropMainVersion, f_cstPropSubVersion, f_cstPropLen, f_cstPropProp, f_reserved3, f_etbCnt, f_etbInfoList,
                      f_etbId, f_cnCnt, f_etbInfoReserved1, f_reserved4, f_vehCnt, f_vehInfoList, f_vehId, f_vehType, f_vehOrient,
                      f_cstVehNo, f_tractVeh, f_vehReserved1,f_vehProp,f_vehPropMainVersion,f_vehPropSubVersion,f_vehPropLen,f_vehPropProp,
                      f_reserved5, f_fctCnt, f_fctInfoList, f_fctName, f_fctId, f_grp, f_fctReserved1, f_fctCstVehNo,f_fctEtbId,f_fctCnId,
                      f_fctReserved2, f_fctProp, f_fctPropmainVersion, f_fctPropSubVersion, f_fctPropLen, f_fctPropProp, f_reserved6,
                      f_cltrCstCnt, f_cltrCstInfoList, f_cltrCstUUID, f_cltrCstOrient, f_cltrCstNo, f_cltrCstReserved1, f_cstTopoCnt,
					  f_version3, f_mainVersion3, f_subVersion3, f_trnCstNo, f_cstCnt, f_cstList, f_cstUUID3, f_cstListCstTopoCnt, f_cstListTrnCstNo,
					  f_cstOrient, f_cstReserved1, f_trnTopoCnt, f_safetyTrail, f_safetyTrailReserved1, f_safetyTrailReserved2,
					  f_safetyTrailVersion, f_safetyTrailMainVersion, f_safetyTrailSubVersion, f_safeSequCount, f_safetyCode} 
   
    function trdp_md_proto.dissector(buf2,pkt2,root2)
        local buffer_len2 = buf2:len()
        if buffer_len2 >= 116 then
            data_type2 = buf2(6,2):uint()
            if  data_type2 ~= 0x4d6e and data_type2 ~= 0x4d72 and data_type2 ~= 0x4d70 and data_type2 ~= 0x4d71 and
                data_type2 ~= 0x4d63 and data_type2 ~= 0x4d65 then
                pkt2.cols.info:set("Fragment of TRDP-MD with TCP protocol or Conflict with the TRDP-MD")
                return
            end
            pkt2.cols.protocol:set("TRDP-MD")
		        local md_headLen = 116
		        local mdTree = root2:add(trdp_md_proto, buf2(0, md_headLen), "TRDP Message Data Header")
            mdTree:append_text("(116 bytes)")
            
--          (1)Sequence Counter
		    local md_offset = 0
            mdTree:add(f_md_sequenceCounter, buf2(0, 4))
 
--          (2)Protocol Version
			md_offset = md_offset + 4
			local md_version = buf2(md_offset, 2):uint()
			temp_version = md_version
			x1 = (temp_version - (temp_version % (16 ^ 2)))
			v1 = x1 / (16 ^ 2)
			temp_version = temp_version - x1
			v2 = temp_version % (16 ^ 2)
			label = string.format("%0#6x", md_version)
			label2 = v1.."."..v2.." ("..label..")"
			mdTree:add(f_md_proVer, buf2(md_offset, 2), label2)
        
--          (3)Msg Type
			md_offset = md_offset + 2
			local md_type = buf2(md_offset, 2):uint()
			if md_type == 0x4d6e then
				mdTree:add(f_md_type, buf2(md_offset, 2), "Mn".." ("..string.format("%0#6x", md_type)..")") 
				pkt2.cols.info:set("MD Notification Message")
			elseif md_type == 0x4d72 then
				mdTree:add(f_md_type, buf2(md_offset, 2), "Mr".." ("..string.format("%0#6x", md_type)..")") 
				pkt2.cols.info:set("MD Request Message")
			elseif md_type == 0x4d70 then
				mdTree:add(f_md_type, buf2(md_offset, 2), "Mp".." ("..string.format("%0#6x", md_type)..")") 
				pkt2.cols.info:set("MD Reply Message without Confirmation")
			elseif md_type == 0x4d71 then
				mdTree:add(f_md_type, buf2(md_offset, 2), "Mq".." ("..string.format("%0#6x", md_type)..")")
				pkt2.cols.info:set("MD Reply Message with Confirmation") 
			elseif md_type == 0x4d63 then
				mdTree:add(f_md_type, buf2(md_offset, 2), "Mc".." ("..string.format("%0#6x", md_type)..")") 
				pkt2.cols.info:set("MD Confirmation Message")
			elseif md_type == 0x4d65 then
				mdTree:add(f_md_type, buf2(md_offset, 2), "Me".." ("..string.format("%0#6x", md_type)..")") 
				pkt2.cols.info:set("MD Error Message")
			else
				mdTree:add(f_md_type, buf2(md_offset, 2))
			end
        
--          (4)Com ID
			md_offset = md_offset + 2
			local comId = buf2(md_offset,4):uint()
			mdTree:add(f_md_comId, buf2(md_offset, 4))        
        
--          (5)etbTopo Count
			md_offset = md_offset + 4
			mdTree:add(f_md_etbTopoCnt, buf2(md_offset, 4))       
				
 --         (6)opTrnTopo Count
			md_offset = md_offset + 4
			mdTree:add(f_md_opTrnTopoCnt, buf2(md_offset, 4)) 
				
--          (7)Dataset Length
			md_offset = md_offset + 4
			mdTree:add(f_md_datasetLength, buf2(md_offset, 4))    
        
--          (8)Reply Status
			md_offset = md_offset + 4
			mdTree:add(f_md_replyStatus, buf2(md_offset, 4))          
        
--          (9)Session ID
			md_offset = md_offset + 4
			mdTree:add(f_md_sessionId, buf2(md_offset, 16))   
        
--          (10)Reply Timeout
			md_offset = md_offset + 16
			mdTree:add(f_md_replyTimeout, buf2(md_offset, 4))         
        
--          (11)Source URI
			md_offset = md_offset + 4
			mdTree:add(f_md_sourceURI, buf2(md_offset, 32))    
        
--          (12)Destination URI
			md_offset = md_offset + 32
			mdTree:add(f_md_destURI, buf2(md_offset, 32))      
	
--          (13)Head FCS
			md_offset = md_offset + 32
			mdTree:add(f_md_headFCS, buf2(md_offset, 4))   
		            
					
--          (14)Dataset        
			md_offset = md_offset + 4
			local data_len2 = buf2:len() - 116                    
			local datasetTree2 = root2:add(trdp_md_proto, buf2(116, data_len2), "TRDP Message Data Dataset")
			datasetTree2:append_text(" ("..data_len2.." bytes)")
--CST_INFO COMID=2			
			if data_len2 > 0 then 
				if comId == 2 then	
					local cstInfo = datasetTree2:add(trdp_md_proto, buf2(116, data_len2), "Consist Info Telegram")		
--version					
					local version = cstInfo:add(f_version, buf2(md_offset,2),"")
					version:add(f_mainVersion,buf2(md_offset,1))
					md_offset = md_offset + 1
					version:add(f_subVersion,buf2(md_offset,1))
--cstClass
					md_offset = md_offset + 1
					cstInfo:add(f_cstClass, buf2(md_offset,1))
--reserved1
					md_offset = md_offset + 1
					cstInfo:add(f_reserved1, buf2(md_offset,1))
--cstId 
					md_offset = md_offset + 1
					cstInfo:add(f_cstId, buf2(md_offset,16))
--cstType
					md_offset = md_offset + 16
					cstInfo:add(f_cstType, buf2(md_offset,16))
--cstOwner
					md_offset = md_offset + 16
					cstInfo:add(f_cstOwner, buf2(md_offset,16))
--cstUUid
					md_offset = md_offset + 16
					local uuid = {}
					for i = 0,15 do
						uuid[i] = buf2(md_offset+i,1)
					end
					label2 = uuid[0]..uuid[1]..uuid[2]..uuid[3]..uuid[4].."-"..uuid[5]..uuid[6].."-"..uuid[7]..uuid[8].."-"..uuid[9]..uuid[10].."-"..uuid[11]..uuid[12]..uuid[13]..uuid[14]..uuid[15]
					cstInfo:add(f_cstUUID, buf2(md_offset,16),label2)
--reserved2
					md_offset = md_offset + 16
					cstInfo:add(f_reserved2, buf2(md_offset,4))
--cstProp
					md_offset = md_offset + 4
					cstPropLen2=4 + buf2(md_offset + 2,2):uint()
					local cstProp = cstInfo:add(f_cstProp, buf2(md_offset, cstPropLen2),"")
					cstProp:add(f_cstPropMainVersion, buf2(md_offset,1))
					md_offset = md_offset + 1
					cstProp:add(f_cstPropSubVersion, buf2(md_offset,1))
					md_offset = md_offset + 1
					cstProp:add(f_cstPropLen, buf2(md_offset,2))
					cstPropLen = buf2(md_offset,2):uint()
					md_offset = md_offset + 2
					cstProp:add(f_cstPropProp, buf2(md_offset,cstPropLen))
--reserved3
					md_offset = md_offset + cstPropLen
					cstInfo:add(f_reserved3, buf2(md_offset,2))
--etbCnt
					md_offset = md_offset + 2
					cstInfo:add(f_etbCnt, buf2(md_offset,2))
					etbCnt = buf2(md_offset,2):uint()
--etbInfoList           
					md_offset = md_offset + 2
					if etbCnt == 0 then
					cstInfo:add(f_etbInfoList, buf2(md_offset,0), string.format("None"))
					elseif etbCnt > 0 then
						for i = 1,etbCnt do
							local  etbInfoList = cstInfo:add(f_etbInfoList, buf2(md_offset,4), string.format("List[%d]", i))
							etbInfoList:add(f_etbId,buf2(md_offset,1))
							md_offset = md_offset + 1
							etbInfoList:add(f_cnCnt,buf2(md_offset,1))
							md_offset = md_offset + 1
							etbInfoList:add(f_etbInfoReserved1,buf2(md_offset,2))
							md_offset = md_offset + 2
						end
					end
--reserved4
					cstInfo:add(f_reserved4, buf2(md_offset,2))
--vehCnt
					md_offset = md_offset + 2
					cstInfo:add(f_vehCnt, buf2(md_offset,2))
					vehCnt = buf2(md_offset,2):uint()
--vehInfoList
					md_offset = md_offset + 2
					if vehCnt == 0 then
						cstInfo:add(f_vehInfoList, buf2(md_offset,0), string.format("None"))
					elseif vehCnt > 0 then
						for i = 1,vehCnt do
							local vehInfo = cstInfo:add(f_vehInfoList, buf2(md_offset,40 + buf2(md_offset+38,2):uint()), string.format("List[%d]", i))
							vehInfo:add(f_vehId,buf2(md_offset,16))
							md_offset = md_offset + 16
							vehInfo:add(f_vehType,buf2(md_offset,16))
							md_offset = md_offset + 16
							vehInfo:add(f_vehOrient,buf2(md_offset,1))
							md_offset = md_offset + 1
							vehInfo:add(f_cstVehNo,buf2(md_offset,1))
							md_offset = md_offset + 1
							vehInfo:add(f_tractVeh,buf2(md_offset,1))
							md_offset = md_offset + 1
							vehInfo:add(f_vehReserved1,buf2(md_offset,1))
							md_offset = md_offset + 1
							local vehProp = vehInfo:add(f_vehProp,buf2(md_offset, 4 + buf2(md_offset+2,2):uint()),"")
							vehProp:add(f_vehPropMainVersion,buf2(md_offset,1))
							md_offset = md_offset + 1
							vehProp:add(f_vehPropSubVersion,buf2(md_offset,1))
							md_offset = md_offset + 1
							vehProp:add(f_vehPropLen,buf2(md_offset,2))
							vehPropLen = buf2(md_offset,2):uint()
							md_offset = md_offset + 2
							vehProp:add(f_vehPropProp,buf2(md_offset,vehPropLen))
							md_offset = md_offset + vehPropLen
						end
					end
--reserved5
					cstInfo:add(f_reserved5, buf2(md_offset,2))
--fctCnt                
					md_offset = md_offset + 2
					cstInfo:add(f_fctCnt, buf2(md_offset,2))
					fctCnt = buf2(md_offset,2):uint()
--fctInfoList
					md_offset = md_offset + 2
					if fctCnt == 0 then
						cstInfo:add(f_fctInfoList, buf2(md_offset,0), string.format("None"))
					elseif fctCnt > 0 then
						for i = 1,fctCnt do
							local fctInfoList = cstInfo:add(f_fctInfoList, buf2(md_offset, 24), string.format("List[%d]", i))
							fctInfoList:add(f_fctName,buf2(md_offset,16))
							md_offset = md_offset + 16
							fctInfoList:add(f_fctId,buf2(md_offset,2))
							md_offset = md_offset + 2
							fctInfoList:add(f_grp,buf2(md_offset,1))
							md_offset = md_offset + 1
							fctInfoList:add(f_fctReserved1,buf2(md_offset,1))
							md_offset = md_offset + 1
							fctInfoList:add(f_fctCstVehNo,buf2(md_offset,1))
							md_offset = md_offset + 1
							fctInfoList:add(f_fctEtbId,buf2(md_offset,1))
							md_offset = md_offset + 1
							fctInfoList:add(f_fctCnId,buf2(md_offset,1))
							md_offset = md_offset + 1
							fctInfoList:add(f_fctReserved2,buf2(md_offset,1))
							md_offset = md_offset + 1
						
--					    	local fctProp = fctInfoList:add(f_fctProp,buf2(md_offset,0),"")
--					    	fctProp:add(f_fctPropmainVersion,buf2(md_offset,1))
--					    	md_offset = md_offset + 1
--					    	fctProp:add(f_fctPropsubVersion,buf2(md_offset,1))
--					    	md_offset = md_offset + 1
--					    	fctProp:add(f_fctPropLen,buf2(md_offset,2))
--					    	fctPropLen = buf2(md_offset,2):uint()
--					    	md_offset = md_offset + 2
--					    	fctProp:add(f_fctvehPropProp,buf2(md_offset,fctPropLen))
--					    	md_offset = md_offset + fctPropLen
						end
					end
--reserved6
				    cstInfo:add(f_reserved6, buf2(md_offset,2))	
				
--cltrCstCnt
					md_offset = md_offset + 2
					cstInfo:add(f_cltrCstCnt, buf2(md_offset,2))
					cltrCstCnt = buf2(md_offset,2):uint()
				
--cltrCstInfoList
					md_offset = md_offset + 2
					if cltrCstCnt == 0 then
						cstInfo:add(f_cltrCstInfoList, buf2(md_offset,0), string.format("None"))
					elseif cltrCstCnt>0 then
						for i = 1,cltrCstCnt do
							local cltrCstInfoList = cstInfo:add(f_cltrCstInfoList, buf2(md_offset,20), string.format("List[%d]", i))
							local uuid = {}
							for i = 0,15 do
								uuid[i] = buf2(md_offset+i,1)
							end
						label2 = uuid[0]..uuid[1]..uuid[2]..uuid[3]..uuid[4].."-"..uuid[5]..uuid[6].."-"..uuid[7]..uuid[8].."-"..uuid[9]..uuid[10].."-"..uuid[11]..uuid[12]..uuid[13]..uuid[14]..uuid[15]
						cltrCstInfoList:add(f_cltrCstUUID,buf2(md_offset,16),label2)
						md_offset = md_offset + 16
						cltrCstInfoList:add(f_cltrCstOrient,buf2(md_offset,1))
						md_offset = md_offset + 1
						cltrCstInfoList:add(f_cltrCstNo,buf2(md_offset,1))
						md_offset = md_offset + 1
						cltrCstInfoList:add(f_cltrCstReserved1,buf2(md_offset,2))
						md_offset = md_offset + 2
						end
					end
--cstTopoCnt
				    cstInfo:add(f_cstTopoCnt, buf2(md_offset,4))
				elseif comId == 3 then	
					local cstInfoCtrl = datasetTree2:add(trdp_md_proto, buf2(116, data_len2), "Consist Info Ctrl Telegram")		
--version					
					local version = cstInfoCtrl:add(f_version3, buf2(md_offset,2),"")
					version:add(f_mainVersion3,buf2(md_offset,1))
					md_offset = md_offset + 1
					version:add(f_subVersion3,buf2(md_offset,1))	
--trnCstNo
					md_offset = md_offset + 1
					cstInfoCtrl:add(f_trnCstNo, buf2(md_offset,1))		
--cstCnt
					md_offset = md_offset + 1
					cstInfoCtrl:add(f_cstCnt, buf2(md_offset,1))	
					cstCnt = buf2(md_offset,1):uint()

					md_offset = md_offset + 1
				    if cstCnt == 0 then
						cstInfoCtrl:add(f_cstList, buf2(md_offset,0), string.format("None"))
					elseif cstCnt > 0 then	
						for i = 1,cstCnt do
							local cstList = cstInfoCtrl:add(f_cstList, buf2(md_offset,24), string.format("List[%d]", i))	
							local uuid = {}
							for i = 0,15 do
								uuid[i] = buf2(md_offset+i,1)
							end
							label2 = uuid[0]..uuid[1]..uuid[2]..uuid[3]..uuid[4].."-"..uuid[5]..uuid[6].."-"..uuid[7]..uuid[8].."-"..uuid[9]..uuid[10].."-"..uuid[11]..uuid[12]..uuid[13]..uuid[14]..uuid[15]
							cstList:add(f_cstUUID, buf2(md_offset,16),label2)
							md_offset = md_offset + 16
							cstList:add(f_cstListCstTopoCnt,buf2(md_offset,4))	
							md_offset = md_offset + 4		
							cstList:add(f_cstListTrnCstNo,buf2(md_offset,1))	
							md_offset = md_offset + 1	
							cstList:add(f_cstOrient,buf2(md_offset,1))	
							md_offset = md_offset + 1								
							cstList:add(f_cstReserved1,buf2(md_offset,2))	
							md_offset = md_offset + 2
						end
					end
--trnTopoCnt
					cstInfoCtrl:add(f_trnTopoCnt, buf2(md_offset,4))	
--safetyTrail
					md_offset = md_offset + 4
					local safetyTrail = cstInfoCtrl:add(f_safetyTrail,buf2(md_offset,16), "")
					safetyTrail:add(f_safetyTrailReserved1,buf2(md_offset,4))
					md_offset = md_offset + 4
					safetyTrail:add(f_safetyTrailReserved2,buf2(md_offset,2))
					md_offset = md_offset + 2
					local safetyTrailVersion = safetyTrail:add(f_safetyTrailVersion,buf2(md_offset,2))
					safetyTrailVersion:add(f_safetyTrailMainVersion,buf2(md_offset,1))
					md_offset = md_offset + 1
					safetyTrailVersion:add(f_safetyTrailSubVersion,buf2(md_offset,1))
					md_offset = md_offset + 1
					safetyTrail:add(f_safeSequCount,buf2(md_offset,4))
					md_offset = md_offset + 4
					safetyTrail:add(f_safetyCode,buf2(md_offset,4))
				end 	
			end					
		else
        pkt2.cols.info:set("udp port "..string.format("%05d",md_port).." conflict with the TRDP-MD protocol")
        return  
		end    
    end
  
    local udp_port_table = DissectorTable.get("udp.port")
    local tcp_port_table = DissectorTable.get("tcp.port");

    udp_port_table:add(pd_port,trdp_pd_proto)
    udp_port_table:add(md_port,trdp_md_proto)
	tcp_port_table:add(md_port,trdp_md_proto);
end
