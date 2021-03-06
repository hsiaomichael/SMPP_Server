import sys,struct,time
import PCA_GenLib
import PCA_Parser
import PCA_SMPP_Parameter_Tag
import PCA_DLL

#reload(PCA_GEIP_Parameter_Tag)

##############################################################################
###    Message Handler   	
##############################################################################
class Handler(PCA_Parser.ContentHandler):	
	
 	def __init__(self):
		PCA_Parser.ContentHandler.__init__(self)
	 	
		
	def startElement(self, name, attrs):
		self.TID = ''
		self.SOURCD_ID = "HeartBeat"
	
	def endDocument(self,debugstr,TID,SOURCD_ID ):
        	self.DebugStr = debugstr
        	self.TID = TID
        	self.SOURCD_ID = SOURCD_ID
	
	def getSOURCD_ID(self):	
		return self.SOURCD_ID
		
	
#########################################################################
# 
#
#########################################################################
class Parser(PCA_Parser.Parser):
	
	bind_receiver = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
	bind_receiver_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x01)
	bind_transmitter = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x02)
	bind_transmitter_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x02)
	bind_tranceiver = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x09)
	bind_tranceiver_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x09)
	outbind = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x0b) 
	unbind = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x06) 
	unbind_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x06) 
	submit_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x04) 
	submit_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x04) 
	deliver_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x05) 
	deliver_sm_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x05) 	
	query_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x03) 
	query_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x03) 
	cancel_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x08) 
	cancel_sm_resp =chr(0x80)+chr(0x0)+chr(0x00)+chr(0x08) 
	replace_sm =  chr(0x00)+chr(0x0)+chr(0x00)+chr(0x07) 
	replace_sm_resp=  chr(0x80)+chr(0x0)+chr(0x00)+chr(0x07) 
	enquire_link =  chr(0x00)+chr(0x00)+chr(0x00)+chr(0x15) 
	enquire_link_resp =  chr(0x80)+chr(0x00)+chr(0x00)+chr(0x15) 
 	generic_nack =  chr(0x80)+chr(0x00)+chr(0x00)+chr(0x00) 
	
	command_id_dict = {}
 	command_id_dict[bind_receiver] = 'bind_receiver'
 	command_id_dict[bind_receiver_resp] = 'bind_receiver_resp'
 	command_id_dict[bind_transmitter] = 'bind_transmitter'
 	command_id_dict[bind_transmitter_resp] = 'bind_transmitter_resp'
 	command_id_dict[submit_sm] = 'submit_sm'
 	command_id_dict[submit_sm_resp] = 'submit_sm_resp'
 	command_id_dict[deliver_sm] = 'deliver_sm' 	
 	command_id_dict[deliver_sm_resp] = 'deliver_sm_resp'
 	command_id_dict[enquire_link] = 'enquire_link'
 	command_id_dict[enquire_link_resp] = 'enquire_link_resp'
 	command_id_dict[bind_tranceiver] = 'bind_tranceiver'
 	command_id_dict[bind_tranceiver_resp] = 'bind_tranceiver_resp'
 	
 	command_id_dict[unbind] = 'unbind'
 	command_id_dict[unbind_resp] = 'unbind_resp'
 	
	
	DebugStr = 'na'
	SMS_TYPE='na'
	
	TID = 'na'
	
	Service_Type = 'na'
	SOURCD_ID = 'HeartBeat'
	

	def __init__(self):
		try:
			Msg = "parser __init__"
			PCA_GenLib.WriteLog(Msg,9)
		
			PCA_Parser.Parser.__init__(self)
  			
  			Msg = "parser __init__ ok"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser __init__  :<%s>,<%s>" % (sys.exc_type,sys.exc_value)
			PCA_GenLib.WriteLog(Msg,0)
			raise
	
	def set_handler(self,name,attrs,content):
			
		self._cont_handler.startElement(name, attrs)        		
		self._cont_handler.characters(content)
        	self._cont_handler.endElement(name)
        	
	def parse(self, source):
		try:
			Msg = "parser init"
			PCA_GenLib.WriteLog(Msg,9)	
			self.SOURCD_ID = 'HeartBeat'
			self.DebugStr = 'na'
			orig_data = source
			name = 'none'	
			self.StartParsing = 0
			
			
			#Msg = "DEBUG orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
			#PCA_GenLib.WriteLog(Msg,0)
			
			
			if (source != None) and len(source) > 0: 
				self._cont_handler.startDocument()
				self.StartParsing = 1
				
				name = "command_length"
				attrs = source[0:4]
				content = struct.unpack("!i",attrs)[0]
				command_length = content
				self.set_handler(name,attrs,content)
				
				source = source[4:]
				name = "command_id"
				attrs = source[0:4]				
				content = struct.unpack("!i",attrs)[0]
				try:
					command_id = self.command_id_dict[attrs]
				except:
					command_id  = 'undef'
				        Msg = "undef command_id=<%s>" % content
				        PCA_GenLib.WriteLog(Msg,0)
				
				content = command_id
				self.set_handler(name,attrs,content)
				
				source = source[4:]
				name = "command_status"
				attrs = source[0:4]				
				content = struct.unpack("!i",attrs)[0]
				command_status = content
				self.set_handler(name,attrs,content)
				
				
				source = source[4:]
				name = "sequence_number"
				attrs = source[0:4]				
				content = struct.unpack("!i",attrs)[0]
				self.TID = content
				sequence_number = content
				self.set_handler(name,attrs,content)
				
				
				Msg = "REQ_TID=<%s>,command_length=<%s>,command_id=<%s>,command_status=<%s>,sequence_number=<%s>" % (self.TID,command_length,command_id,command_status,sequence_number)
				PCA_GenLib.WriteLog(Msg,2)
				
				self.DebugStr = Msg
				
				dll_file_name = command_id
				Script_File = PCA_DLL.DLL(dll_file_name)	
					
				factory_function="Parser"
				factory_component = Script_File.symbol(factory_function)
				self.parser = factory_component()
			
				factory_function="Handler"
				factory_component = Script_File.symbol(factory_function)
				self.handler  = factory_component()			
				self.parser.setContentHandler(self.handler )
				
				
				self.parser.parse(source[4:])
				response_message = self.handler.getHandlerResponse()	
				
				
				if command_id == "bind_receiver" or command_id == "bind_tranceiver":
					address_range = self.handler.getADDRESS_RANGE()
					name = "address_range"
					attrs = address_range
					content = attrs
					self.set_handler(name,attrs,content)
                    
					AIM = self.handler.getSystem_ID()
					name = "system_id"
					attrs = AIM
					content = attrs
					self.set_handler(name,attrs,content)
					
				elif command_id == "submit_sm":
					dest_address = self.handler.getDEST_ADDR()
					name = "dest_address"
					attrs = dest_address
					content = attrs
					self.set_handler(name,attrs,content)
					TXT = self.handler.getTXT()
					name = "TXT"
					attrs = TXT
					content = attrs
					self.set_handler(name,attrs,content)
				        message_id = response_message
					name = "message_id"
					attrs = message_id
					content = attrs
					self.set_handler(name,attrs,content)
					DELIVER_SM_PDU = self.handler.getDELIVER_SM_PDU()
					name = "DELIVER_SM_PDU"
					attrs = DELIVER_SM_PDU
					content = attrs
					self.set_handler(name,attrs,content)
					#Msg = "set DELIVER_SM_PDU"
					#PCA_GenLib.WriteLog(Msg,0)
				
				DebugStr = self.handler.getDebugStr()
				self.DebugStr = "%s %s" % (self.DebugStr , DebugStr)
				
				
			if self.StartParsing == 1:
        			self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID,response_message)
        		
        		
			Msg = "parser OK"
			PCA_GenLib.WriteLog(Msg,9)
		except:
 			Msg = "parser  :<%s>,<%s>,name=<%s>" % (sys.exc_type,sys.exc_value,name)
			PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "orig data =\n%s" % PCA_GenLib.HexDump(orig_data)
			PCA_GenLib.WriteLog(Msg,0)
			
			Msg = "rest data =\n%s" % PCA_GenLib.HexDump(source)
			PCA_GenLib.WriteLog(Msg,0)
			if self.StartParsing == 1:
        			self._cont_handler.endDocument(self.DebugStr,self.TID,self.SOURCD_ID,'undef')
        		raise
	        		
	        		
