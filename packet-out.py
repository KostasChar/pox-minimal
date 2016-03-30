
from pox.core import core
import pox.openflow.libopenflow_01 as of

mac_table={}

def _handle_PacketIn (event):
  packet = event.parsed
  mac_table[packet.src] = event.port
  if packet.dst not in mac_table.keys():
    msg = of.ofp_packet_out(data=event.ofp) 
    msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD)) 
    event.connection.send(msg)
  if packet.dst in mac_table.keys():
    msg = of.ofp_packet_out(data=event.ofp) 
    msg.actions.append(of.ofp_action_output(port = mac_table.get(packet.dst)))
    event.connection.send(msg)


def launch ():
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
