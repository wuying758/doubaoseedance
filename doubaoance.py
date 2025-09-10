import os
from volcenginesdkarkruntime import Ark
import argparse
import time
from tqdm import tqdm
from utils import *
from frame import *

current_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
print(f"Current time: {current_time}")
print(f"Default save path: ./outputs/{current_time}")
#argparse输入参数
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--api_key", type=str, required=False, help="Your API Key", default="7d55967c-94d4-4f3d-bd67-61a2d675cf18", )
parser.add_argument('-p', '--save_path', type=str, required=False, help='Path to save', default="./outputs/")
parser.add_argument('-u', '--base_url', type=str, required=False, help='Base URL for the Ark API', default="https://ark.cn-beijing.volces.com/api/v3")
parser.add_argument('-r', '--prompt', type=str, required=False, help='Prompt for image generation',default="None")
parser.add_argument('-m', '--model', type=str, required=False, help='Model for image generation', default="doubao-seedance-1-0-lite-i2v-250428")
parser.add_argument('-s', '--seed', type=int, required=False, help='Seed for image generation', default=-1)
parser.add_argument('-z', '--size', type=str, required=False, help='Size of the generated image', default="1280x720")
parser.add_argument('-n', '--num', type=int, required=False, help='Number of images to generate', default=1)
parser.add_argument('-i', '--image_dir', type=str, required=False, help='Directory containing images for image-to-image generation', default="./inputs/")
parser.add_argument('-g', '--guidance_scale', type=float, required=False, help='Guidance scale for image generation', default=5.5)
parser.add_argument('-b', '--bingxing', type=bool , required=False, help='Whether to generate Bingxing image', default=True)
parser.add_argument('-o', '--resolution', type=str, required=False, help='resolution of the video returned', default='480p')
parser.add_argument('-t', '--ratio', type=str, required=False, help='the 宽高比', default='16:9')
parser.add_argument('-j', '--duration', type=int, required=False, help='duration of the video returned', default=3)
parser.add_argument('-f', '--fps', type=int, required=False, help='fps of the video returned', default=24)
parser.add_argument('-y', '--watermark', type=bool, required=False, help='whether to add watermark', default=False)
parser.add_argument('--no_ask', type=bool, required=False, help='whether to ask for confirmation before generating image', default=False)
parser.add_argument('--no_interrupt', type=bool, required=False, help='whether to interrupt the program when an error occurs', default=False)
parser.add_argument('--num_of_frames', type=int, required=False, help='number of frames to extract from the video', default=5)
client = Ark(
    base_url=parser.parse_args().base_url,
    api_key=parser.parse_args().api_key
    )
def enum_utils(args, image_files, image_num):
    for i, img_path in enumerate(tqdm(image_files, desc="Processing images")):
        try:
            create_result_bingxing(args, client, img_path, i, image_num)
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")


def main():
    args = parser.parse_args()
    args.save_path = os.path.join(args.save_path, current_time)
    print(f"Save path: {args.save_path}")
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)
    args_into_txt(args,args.save_path)
    args.prompt = prompt_read(args)
    args.prompt = prompt_edit(args)
    print(f"Create Video using prompt : {args.prompt}")
    print("------ Create request ------")
    if args.bingxing:
        image_num = len(os.listdir(args.image_dir))
        image_files, image_num = image_chuli(args)
        enum_utils(args, image_files, image_num)
        
    else:
        create_result = create_result_no_bingxing(args,client)
        print(f"The id of the result: {create_result.id}")
        print("------ Polling Task Status ------")
        task_id = create_result.id
        result = query_result(args, task_id, client)
        save_path = download_result(args,result)
        image_from_video(save_path, args.num_of_frames)
        print("------ Finish ------")


if __name__ == "__main__":
    main()
