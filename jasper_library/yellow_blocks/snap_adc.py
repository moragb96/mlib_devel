from yellow_block import YellowBlock
from verilog import VerilogModule
from constraints import PortConstraint, ClockConstraint

class snap_adc(YellowBlock):
    def initialize(self):
        # num_units is the number of ADC chips
        # board_count is the number of boards
        self.num_units = 3
        self.num_clocks = 1
        self.zdok_rev = 2 # no frame clocks (see adc16)

        self.clock_freq = self.sample_rate

        self.add_source('adc16_interface')
        self.add_source('wb_adc16_controller')
        self.add_source('wb_bram')

        self.provides = ['adc0_clk','adc0_clk90', 'adc0_clk180', 'adc0_clk270']
        self.requires = ['HAD1511_0', 'HAD1511_1', 'HAD1511_2']

    def modify_top(self,top):
        module = 'adc16_interface'
        inst = top.get_instance(entity=module, name=self.fullname, comment=self.fullname)
        inst.add_parameter('G_NUM_CLOCKS', int(self.num_clocks))
        inst.add_parameter('G_ZDOK_REV', int(self.zdok_rev))
        inst.add_parameter('G_NUM_UNITS', int(self.num_units))

        # ports which go to simulink
        inst.add_port('a1', self.fullname+'_a1', width=8)
        inst.add_port('a2', self.fullname+'_a2', width=8)
        inst.add_port('a3', self.fullname+'_a3', width=8)
        inst.add_port('a4', self.fullname+'_a4', width=8)
        inst.add_port('b1', self.fullname+'_b1', width=8)
        inst.add_port('b2', self.fullname+'_b2', width=8)
        inst.add_port('b3', self.fullname+'_b3', width=8)
        inst.add_port('b4', self.fullname+'_b4', width=8)
        inst.add_port('c1', self.fullname+'_c1', width=8)
        inst.add_port('c2', self.fullname+'_c2', width=8)
        inst.add_port('c3', self.fullname+'_c3', width=8)
        inst.add_port('c4', self.fullname+'_c4', width=8)

        # ports which go to the wb controller. Any ports which don't go to top level need
        # corresponding signals to be added to top.v
        inst.add_port('fabric_clk', 'adc0_clk')
        inst.add_port('fabric_clk_90', 'adc0_clk90')
        inst.add_port('fabric_clk_180', 'adc0_clk180')
        inst.add_port('fabric_clk_270', 'adc0_clk270')

        inst.add_port('reset', 'adc16_reset')
        inst.add_port('iserdes_bitslip', 'adc16_iserdes_bitslip', width=8)

        inst.add_port('delay_rst', 'adc16_delay_rst', width=64)
        inst.add_port('delay_tap', 'adc16_delay_tap', width=5)

        inst.add_port('snap_req', 'adc16_snap_req')
        inst.add_port('snap_we', 'adc16_snap_we')
        inst.add_port('snap_addr', 'adc16_snap_addr', width=10)

        inst.add_port('locked', 'adc16_locked', width=2)

        # Now the external ports, which need corresponding ports adding to top.v

        inst.add_port('clk_frame_p', '0', parent_sig=False)
        inst.add_port('clk_frame_n', '0', parent_sig=False)

        inst.add_port('clk_line_p', 'adc16_clk_line_p', parent_port=True, dir='in', width=self.num_clocks)
        inst.add_port('clk_line_n', 'adc16_clk_line_n', parent_port=True, dir='in', width=self.num_clocks)
        inst.add_port('ser_a_p', 'adc16_ser_a_p', parent_port=True, dir='in', width=4*self.num_units)
        inst.add_port('ser_a_n', 'adc16_ser_a_n', parent_port=True, dir='in', width=4*self.num_units)
        inst.add_port('ser_b_p', 'adc16_ser_b_p', parent_port=True, dir='in', width=4*self.num_units)
        inst.add_port('ser_b_n', 'adc16_ser_b_n', parent_port=True, dir='in', width=4*self.num_units)


        # wb controller

        wbctrl = top.get_instance(entity='wb_adc16_controller', name='wb_adc16_controller')
        wbctrl.add_parameter('G_ROACH2_REV', 0)
        wbctrl.add_parameter('G_ZDOK_REV', int(self.zdok_rev))
        wbctrl.add_parameter('G_NUM_UNITS', int(self.num_units))
        wbctrl.add_parameter('G_NUM_SCLK_LINES', 3)
        wbctrl.add_parameter('G_NUM_SDATA_LINES', 3)
        # These are top-level ports -- they don't need signal declarations,
        # but they do need ports added to the top-level
        wbctrl.add_port('adc0_adc3wire_csn1', 'adc0_adc3wire_csn1', dir='out', parent_port=True)
        wbctrl.add_port('adc0_adc3wire_csn2', 'adc0_adc3wire_csn2', dir='out', parent_port=True)
        wbctrl.add_port('adc0_adc3wire_csn3', 'adc0_adc3wire_csn3', dir='out', parent_port=True)
        wbctrl.add_port('adc0_adc3wire_csn4', '')
        wbctrl.add_port('adc0_adc3wire_sdata','adc0_adc3wire_sdata', width=3, dir='out', parent_port=True)
        wbctrl.add_port('adc0_adc3wire_sclk', 'adc0_adc3wire_sclk', width=3, dir='out', parent_port=True)
        wbctrl.add_port('adc1_adc3wire_csn1', '')
        wbctrl.add_port('adc1_adc3wire_csn2', '')
        wbctrl.add_port('adc1_adc3wire_csn3', '')
        wbctrl.add_port('adc1_adc3wire_csn4', '')
        wbctrl.add_port('adc1_adc3wire_sdata','')
        wbctrl.add_port('adc1_adc3wire_sclk', '')

        # internal connections to the adc controller. We have already declared the corresponding
        # signals earlier.
        wbctrl.add_port('adc16_reset','adc16_reset')
        wbctrl.add_port('adc16_iserdes_bitslip','adc16_iserdes_bitslip', width=8)
        wbctrl.add_port('adc16_delay_rst', 'adc16_delay_rst', width=64)
        wbctrl.add_port('adc16_delay_tap', 'adc16_delay_tap', width=5)
        wbctrl.add_port('adc16_snap_req',  'adc16_snap_req')
        wbctrl.add_port('adc16_locked',    'adc16_locked', width=2)
        # and finally the wb interface
        wbctrl.add_wb_interface(nbytes=2**8, regname='adc16_controller', mode='rw')

        snap_chan = ['a','b','c','d','e','f','g','h']
        for k in range(self.num_units):
            # Embedded wb-RAM
            din = self.fullname+'_%s'%snap_chan[k]
            wbram = top.get_instance(entity='wb_bram', name='adc16_wb_ram%d'%k, comment='Embedded ADC16 bram')
            wbram.add_parameter('LOG_USER_WIDTH','5')
            wbram.add_parameter('USER_ADDR_BITS','10')
            wbram.add_parameter('N_REGISTERS','2')
            wbram.add_wb_interface(regname='adc16_wb_ram%d'%k, mode='rw', nbytes=4*2**10)
            wbram.add_port('user_clk','user_clk')
            wbram.add_port('user_addr','adc16_snap_addr', width=10)
            wbram.add_port('user_din','{%s1, %s2, %s3, %s4}'%(din,din,din,din), parent_sig=False)
            wbram.add_port('user_we','adc16_snap_we')
            wbram.add_port('user_dout','')

    def gen_constraints(self):
        cons = []
        # ADC SPI interface
        cons.append(PortConstraint('adc0_adc3wire_csn1',   'adc_csn', iogroup_index=0))
        cons.append(PortConstraint('adc0_adc3wire_csn2',   'adc_csn', iogroup_index=1))
        cons.append(PortConstraint('adc0_adc3wire_csn3',   'adc_csn', iogroup_index=2))
        cons.append(PortConstraint('adc0_adc3wire_sdata', 'adc_sdata', port_index=range(3), iogroup_index=range(3)))
        cons.append(PortConstraint('adc0_adc3wire_sclk',  'adc_sclk', port_index=range(3), iogroup_index=range(3)))

        cons.append(PortConstraint('adc16_clk_line_p',  'adc_lclkp', iogroup_index=0))
        cons.append(PortConstraint('adc16_clk_line_n',  'adc_lclkn', iogroup_index=0))

        cons.append(PortConstraint('adc16_ser_a_p', 'adc0_out', port_index=range(4), iogroup_index=range(0,16,4)))
        cons.append(PortConstraint('adc16_ser_a_n', 'adc0_out', port_index=range(4), iogroup_index=range(1,16,4)))
        cons.append(PortConstraint('adc16_ser_b_p', 'adc0_out', port_index=range(4), iogroup_index=range(2,16,4)))
        cons.append(PortConstraint('adc16_ser_b_n', 'adc0_out', port_index=range(4), iogroup_index=range(3,16,4)))

        cons.append(PortConstraint('adc16_ser_a_p', 'adc1_out', port_index=range(4,8), iogroup_index=range(0,16,4)))
        cons.append(PortConstraint('adc16_ser_a_n', 'adc1_out', port_index=range(4,8), iogroup_index=range(1,16,4)))
        cons.append(PortConstraint('adc16_ser_b_p', 'adc1_out', port_index=range(4,8), iogroup_index=range(2,16,4)))
        cons.append(PortConstraint('adc16_ser_b_n', 'adc1_out', port_index=range(4,8), iogroup_index=range(3,16,4)))

        cons.append(PortConstraint('adc16_ser_a_p', 'adc2_out', port_index=range(8,12), iogroup_index=range(0,16,4)))
        cons.append(PortConstraint('adc16_ser_a_n', 'adc2_out', port_index=range(8,12), iogroup_index=range(1,16,4)))
        cons.append(PortConstraint('adc16_ser_b_p', 'adc2_out', port_index=range(8,12), iogroup_index=range(2,16,4)))
        cons.append(PortConstraint('adc16_ser_b_n', 'adc2_out', port_index=range(8,12), iogroup_index=range(3,16,4)))
        
        # clock constraint with variable period
        cons.append(ClockConstraint('adc16_clk_line_p', name='adc_clk', freq=self.clock_freq))

        return cons

        
