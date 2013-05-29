function twiddle_coeff_0_init(blk, varargin)

  clog('entering twiddle_coeff_0_init',{'trace', 'twiddle_coeff_0_init_debug'});

  defaults = { ...
    'n_inputs', 1, ...
    'add_latency', 1, ...
    'mult_latency', 2, ...
    'bram_latency', 2, ...
    'conv_latency', 2, ...
    'async', 'off'};

  if same_state(blk, 'defaults', defaults, varargin{:}), return, end
  check_mask_type(blk, 'twiddle_coeff_0');
  munge_block(blk, varargin{:});

  delete_lines(blk);

  n_inputs       = get_var('n_inputs', 'defaults', defaults, varargin{:});
  add_latency    = get_var('add_latency', 'defaults', defaults, varargin{:});
  bram_latency   = get_var('bram_latency', 'defaults', defaults, varargin{:});
  mult_latency   = get_var('mult_latency', 'defaults', defaults, varargin{:});
  conv_latency   = get_var('conv_latency', 'defaults', defaults, varargin{:});
  async          = get_var('async', 'defaults', defaults, varargin{:});

  if n_inputs == 0,
    clean_blocks(blk);
    save_state(blk, 'defaults', defaults, varargin{:});
    clog('exiting twiddle_coeff_0_init', {'trace', 'twiddle_coeff_0_init_debug'});
    return;
  end
  
  reuse_block(blk, 'ai', 'built-in/Inport');
  set_param([blk,'/ai'], ...
          'Port', sprintf('1'), ...
          'Position', sprintf('[145 28 175 42]'));

  reuse_block(blk, 'bi', 'built-in/Inport');
  set_param([blk,'/bi'], ...
          'Port', sprintf('2'), ...
          'Position', sprintf('[145 93 175 107]'));

  reuse_block(blk, 'sync_in', 'built-in/Inport');
  set_param([blk,'/sync_in'], ...
          'Port', sprintf('3'), ...
          'Position', sprintf('[145 163 175 177]'));

  reuse_block(blk, 'delay0', 'xbsIndex_r4/Delay');
  set_param([blk,'/delay0'], ...
          'latency', sprintf('mult_latency+add_latency+bram_latency+conv_latency'), ...
          'reg_retiming', sprintf('on'), ...
          'Position', sprintf('[195 14 235 56]'));

  reuse_block(blk, 'delay1', 'xbsIndex_r4/Delay');
  set_param([blk,'/delay1'], ...
          'latency', sprintf('mult_latency+add_latency+bram_latency+conv_latency'), ...
          'reg_retiming', sprintf('on'), ...
          'Position', sprintf('[195 79 235 121]'));

  reuse_block(blk, 'delay2', 'xbsIndex_r4/Delay');
  set_param([blk,'/delay2'], ...
          'latency', sprintf('mult_latency+add_latency+bram_latency+conv_latency'), ...
          'reg_retiming', sprintf('on'), ...
          'Position', sprintf('[195 149 235 191]'));

  reuse_block(blk, 'ao', 'built-in/Outport');
  set_param([blk,'/ao'], ...
          'Port', sprintf('1'), ...
          'Position', sprintf('[255 28 285 42]'));

  reuse_block(blk, 'bwo', 'built-in/Outport');
  set_param([blk,'/bwo'], ...
          'Port', sprintf('2'), ...
          'Position', sprintf('[255 93 285 107]'));

  reuse_block(blk, 'sync_out', 'built-in/Outport');
  set_param([blk,'/sync_out'], ...
          'Port', sprintf('3'), ...
          'Position', sprintf('[255 163 285 177]'));

  add_line(blk,'bi/1','delay1/1', 'autorouting', 'on');
  add_line(blk,'sync_in/1','delay2/1', 'autorouting', 'on');
  add_line(blk,'ai/1','delay0/1', 'autorouting', 'on');
  add_line(blk,'delay0/1','ao/1', 'autorouting', 'on');
  add_line(blk,'delay1/1','bwo/1', 'autorouting', 'on');
  add_line(blk,'delay2/1','sync_out/1', 'autorouting', 'on');
  
  if strcmp(async, 'on'),
    reuse_block(blk, 'dvi', 'built-in/Inport', ...
            'Port', '4', ...
            'Position', [145 163+65 175 177+65]);
    reuse_block(blk, 'delay3', 'xbsIndex_r4/Delay', ...
            'latency', 'mult_latency+add_latency+bram_latency+conv_latency', ...
            'reg_retiming', 'on', ...
            'Position', [195 149+65 235 191+65]);
    reuse_block(blk, 'dvo', 'built-in/Outport', ...
            'Port', '4', ...
            'Position', [255 163+65 285 177+65]);
    add_line(blk, 'dvi/1', 'delay3/1');
    add_line(blk, 'delay3/1', 'dvo/1');
  end

  clean_blocks(blk);

  save_state(blk, 'defaults', defaults, varargin{:});
  clog('exiting twiddle_coeff_0_init', {'trace','twiddle_coeff_0_init_debug'});
end % twiddle_coeff_0_init
