# -*- coding:utf8 -*-

###########################################
# Date: 2012                              #
# Auteur: Malphaet                        #
# Nom: redPrint                           #
# Version: 0.3a                           #
# Copyright 2011: infiniteWander          #
###########################################
# This file is part of redPrint.
#
# redPrint is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# redPrint is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with redPrint. If not, see <http://www.gnu.org/licenses/>.
########################################################
# LICENCE                                              #
########################################################

######################
#----- Modules ------#
######################

#---- Importation ---#

import ConfigParser,argparse
import sys,os,shutil
from PIL import Image,ImageChops

#------ Ajouts ------#
#CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(CURRENT_DIR,'Modules'))

#from functions import *

######################
#     Functions      #
######################
import numpy as np

def alpha_composite(src, dst):
    '''
    Return the alpha composite of src and dst.

    Parameters:
    src -- PIL RGBA Image object
    dst -- PIL RGBA Image object

    The algorithm comes from http://en.wikipedia.org/wiki/Alpha_compositing
    '''
    # http://stackoverflow.com/a/3375291/190597
    # http://stackoverflow.com/a/9166671/190597
    src = np.asarray(src)
    dst = np.asarray(dst)
    out = np.empty(src.shape, dtype = 'float')
    alpha = np.index_exp[:, :, 3:]
    rgb = np.index_exp[:, :, :3]
    src_a = src[alpha]/255.0
    dst_a = dst[alpha]/255.0
    out[alpha] = src_a+dst_a*(1-src_a)
    old_setting = np.seterr(invalid = 'ignore')
    out[rgb] = (src[rgb]*src_a + dst[rgb]*dst_a*(1-src_a))/out[alpha]
    np.seterr(**old_setting)    
    out[alpha] *= 255
    np.clip(out,0,255)
    # astype('uint8') maps np.nan (and np.inf) to 0
    out = out.astype('uint8')
    out = Image.fromarray(out, 'RGBA')
    return out
######################
#    Main Program    #
######################

parser=argparse.ArgumentParser(description="Read a config file, make an image from it")
#parser.add_argument('conf', metavar='config', nargs='1', type=str,help='a config file to apply')
parser.add_argument('-v','--verbose', dest='VV', action='store_const', const=True, help='be verbose')
parser.add_argument('-f','--force', dest='OVERWRITE', action='store_const', const=True, default=False, help='overwrite destination data')
args = parser.parse_args()

im = Image.open("Images/Background/RedPrint-BG.png")
im2 = Image.open("Images/Background/Overlay.png")

loo=alpha_composite(im2,im)
loo.save('mooo.png')
