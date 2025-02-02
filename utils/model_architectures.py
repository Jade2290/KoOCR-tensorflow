import tensorflow as tf
import numpy as np
import utils.korean_manager as korean_manager
import utils.CustomLayers as CustomLayers
from utils.model_components import build_FC,PreprocessingPipeline

def VGG16(settings):
    if settings['direct_map']:
        input_channels=8
    else:
        input_channels=1
    VGG_net = tf.keras.applications.VGG16(input_shape=(settings['input_shape'],settings['input_shape'],input_channels),
                                               include_top=False,weights=None)

    input_image=tf.keras.layers.Input(shape=(settings['input_shape'],settings['input_shape']),name='input_image')
    preprocessed=tf.keras.layers.Reshape((settings['input_shape'],settings['input_shape'],1))(input_image)
    preprocessed=PreprocessingPipeline(settings['direct_map'],settings['data_augmentation'])(preprocessed)
    
    feature=VGG_net(preprocessed)
    
    return build_FC(input_image,x,settings)

def EfficientCNN(settings):
    def fire_block(x,channels,stride=1):
        fire=tf.keras.layers.Conv2D(channels//8,kernel_size=1,padding='same')(x)
        firel=tf.keras.layers.BatchNormalization()(fire)
        fire=tf.keras.layers.LeakyReLU()(fire)

        fire1=tf.keras.layers.Conv2D(channels//2,kernel_size=3,padding='same',strides=(stride,stride))(fire)
        fire1=tf.keras.layers.BatchNormalization()(fire1)
        fire1=tf.keras.layers.LeakyReLU()(fire1)

        fire2=tf.keras.layers.Conv2D(channels//2,kernel_size=3,padding='same',strides=(stride,stride))(fire)
        fire2=tf.keras.layers.BatchNormalization()(fire2)
        fire2=tf.keras.layers.LeakyReLU()(fire2)

        fire=tf.keras.layers.concatenate([fire1,fire2])
        return fire

    input_image=tf.keras.layers.Input(shape=(settings['input_shape'],settings['input_shape']),name='input_image')
    preprocessed=tf.keras.layers.Reshape((settings['input_shape'],settings['input_shape'],1))(input_image)
    preprocessed=PreprocessingPipeline(settings['direct_map'],settings['data_augmentation'])(preprocessed)

    conv1=tf.keras.layers.Conv2D(64,kernel_size=3,padding='same')(preprocessed)
    conv1=tf.keras.layers.BatchNormalization()(conv1)
    conv1=tf.keras.layers.LeakyReLU()(conv1)

    fire1=fire_block(conv1,64,2)
    fire2=fire_block(fire1,128)
    fire3=fire_block(fire2,128)
    fire4=fire_block(fire3,128,2)
    fire5=fire_block(fire4,256)
    fire6=fire_block(fire5,256)
    fire7=fire_block(fire6,256,2)
    fire8=fire_block(fire7,512)
    fire9=fire_block(fire8,512)
    fire10=fire_block(fire9,512)
    fire11=fire_block(fire10,512)

    return build_FC(input_image,fire11,settings)
    
def InceptionResnetV2(settings):
    if settings['direct_map']:
        input_channels=8
    else:
        input_channels=1
    InceptionResnet = tf.keras.applications.InceptionResNetV2(input_shape=(settings['input_shape'],settings['input_shape'],input_channels),
                                               include_top=False,weights=None)

    input_image=tf.keras.layers.Input(shape=(settings['input_shape'],settings['input_shape']),name='input_image')
    preprocessed=tf.keras.layers.Reshape((settings['input_shape'],settings['input_shape'],1))(input_image)
    preprocessed=PreprocessingPipeline(settings['direct_map'],settings['data_augmentation'])(preprocessed)

    feature=InceptionResnet(preprocessed)
    
    return build_FC(input_image,x,settings)

def MobilenetV3(settings):
    if settings['direct_map']:
        input_channels=8
    else:
        input_channels=1
    Mobilenet = tf.keras.applications.MobileNetV3Small(input_shape=(settings['input_shape'],settings['input_shape'],input_channels),
                                               include_top=False, weights=None)

    input_image=tf.keras.layers.Input(shape=(settings['input_shape'],settings['input_shape']),name='input_image')
    preprocessed=tf.keras.layers.Reshape((settings['input_shape'],settings['input_shape'],1))(input_image)
    preprocessed=PreprocessingPipeline(settings['direct_map'],settings['data_augmentation'])(preprocessed)
    
    feature=Mobilenet(preprocessed)
    
    return build_FC(input_image,x,settings)

def AFL_Model(settings):
    if settings['direct_map']:
        input_channels=8
    else:
        input_channels=1
    input_image=tf.keras.layers.Input(shape=(settings['input_shape'],settings['input_shape']),name='input_image')
    preprocessed=tf.keras.layers.Reshape((settings['input_shape'],settings['input_shape'],1))(input_image)
    preprocessed=PreprocessingPipeline(settings['direct_map'],settings['data_augmentation'])(preprocessed)
    
    def conv_block(channels,kernel_size=3,strides=1,bn=True):
        m=tf.keras.models.Sequential([
            tf.keras.layers.Conv2D(channels,kernel_size,strides=strides,padding='same'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.LeakyReLU()
        ])
        return m
    
    x=conv_block(96)(preprocessed)
    x=conv_block(96,strides=2)(x)
    x=conv_block(128)(x)
    x=conv_block(128,strides=2)(x)
    x=conv_block(160)(x)
    x=conv_block(160,strides=2)(x)
    x=conv_block(256)(x)
    x=conv_block(256,strides=2)(x)
    x=conv_block(256)(x)

    return build_FC(input_image,x,settings)