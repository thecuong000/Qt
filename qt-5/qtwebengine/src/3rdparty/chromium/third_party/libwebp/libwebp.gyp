# Copyright (c) 2012 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

{
  'variables': {
    'neon_sources': [
      'dsp/dec_neon.c',
      'dsp/enc_neon.c',
      'dsp/lossless_neon.c',
      'dsp/upsampling_neon.c',
    ]
  },
  'targets': [
    {
      'target_name': 'libwebp_dec',
      'type': 'static_library',
      'dependencies' : [
        'libwebp_dsp',
        'libwebp_dsp_neon',
        'libwebp_utils',
      ],
      'include_dirs': ['.'],
      'sources': [
        'dec/alpha.c',
        'dec/buffer.c',
        'dec/frame.c',
        'dec/idec.c',
        'dec/io.c',
        'dec/quant.c',
        'dec/tree.c',
        'dec/vp8.c',
        'dec/vp8l.c',
        'dec/webp.c',
      ],
    },
    {
      'target_name': 'libwebp_demux',
      'type': 'static_library',
      'include_dirs': ['.'],
      'sources': [
        'demux/demux.c',
      ],
    },
    {
      'target_name': 'libwebp_dsp',
      'type': 'static_library',
      'include_dirs': ['.'],
      'sources': [
        'dsp/alpha_processing.c',
        'dsp/alpha_processing_sse2.c',
        'dsp/cpu.c',
        'dsp/dec.c',
        'dsp/dec_clip_tables.c',
        'dsp/dec_mips32.c',
        'dsp/dec_sse2.c',
        'dsp/enc.c',
        'dsp/enc_avx2.c',
        'dsp/enc_mips32.c',
        'dsp/enc_sse2.c',
        'dsp/lossless.c',
        'dsp/lossless_mips32.c',
        'dsp/lossless_sse2.c',
        'dsp/upsampling.c',
        'dsp/upsampling_sse2.c',
        'dsp/yuv.c',
        'dsp/yuv_mips32.c',
        'dsp/yuv_sse2.c',
      ],
      'conditions': [
        ['OS == "android"', {
          'includes': [ '../../build/android/cpufeatures.gypi' ],
        }],
        ['order_profiling != 0', {
          'target_conditions' : [
            ['_toolset=="target"', {
              'cflags!': [ '-finstrument-functions' ],
            }],
          ],
        }],
      ],
    },
    {
      'target_name': 'libwebp_dsp_neon',
      'conditions': [
        ['target_arch == "arm" and arm_version >= 7 and (arm_neon == 1 or arm_neon_optional == 1)', {
          'type': 'static_library',
          'include_dirs': ['.'],
          'sources': [
            '<@(neon_sources)'
          ],
          # behavior similar to *.c.neon in an Android.mk
          'cflags!': [ '-mfpu=vfpv3-d16' ],
          'cflags': [ '-mfpu=neon' ],
        },{
          'conditions': [
            ['target_arch == "arm64"', {
              'type': 'static_library',
              'include_dirs': ['.'],
              'sources': [
                '<@(neon_sources)'
              ],
              # avoid an ICE with gcc-4.9: b/15574841
              'cflags': [ '-frename-registers' ],
            },{  # "target_arch != "arm|arm64" or arm_version < 7"
              'type': 'none',
            }],
          ],
        }],
        ['order_profiling != 0', {
          'target_conditions' : [
            ['_toolset=="target"', {
              'cflags!': [ '-finstrument-functions' ],
            }],
          ],
        }],
      ],
    },
    {
      'target_name': 'libwebp_enc',
      'type': 'static_library',
      'include_dirs': ['.'],
      'sources': [
        'enc/alpha.c',
        'enc/analysis.c',
        'enc/backward_references.c',
        'enc/config.c',
        'enc/cost.c',
        'enc/filter.c',
        'enc/frame.c',
        'enc/histogram.c',
        'enc/iterator.c',
        'enc/picture.c',
        'enc/picture_csp.c',
        'enc/picture_psnr.c',
        'enc/picture_rescale.c',
        'enc/picture_tools.c',
        'enc/quant.c',
        'enc/syntax.c',
        'enc/token.c',
        'enc/tree.c',
        'enc/vp8l.c',
        'enc/webpenc.c',
      ],
    },
    {
      'target_name': 'libwebp_utils',
      'type': 'static_library',
      'include_dirs': ['.'],
      'sources': [
        'utils/bit_reader.c',
        'utils/bit_writer.c',
        'utils/color_cache.c',
        'utils/filters.c',
        'utils/huffman.c',
        'utils/huffman_encode.c',
        'utils/quant_levels.c',
        'utils/quant_levels_dec.c',
        'utils/random.c',
        'utils/rescaler.c',
        'utils/thread.c',
        'utils/utils.c',
      ],
    },
    {
      'target_name': 'libwebp',
      'type': 'none',
      'dependencies' : [
        'libwebp_dec',
        'libwebp_demux',
        'libwebp_dsp',
        'libwebp_dsp_neon',
        'libwebp_enc',
        'libwebp_utils',
      ],
      'direct_dependent_settings': {
        'include_dirs': ['.'],
      },
      'conditions': [
        ['OS!="win"', {'product_name': 'webp'}],
      ],
    },
  ],
}
