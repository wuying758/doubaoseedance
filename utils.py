import requests
import base64
import os
import time
import glob
import argparse
import sys
import shutil
from frame import image_from_video
def download_result(args,result,number=-1):
    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    if result.status != "succeeded":
        print("Task did not succeed, no results to download.")
        return
    if args.bingxing:
        outdir = number
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        if result.content.video_url:
            filename = f"video.mp4"
            save_path = os.path.join(outdir,filename)
            download(args,result.content.video_url,save_path,number)
    else:
        filename = f"video.mp4"
        save_path = os.path.join(args.save_path,filename)
        download(args,result.content.video_url,save_path,number)
    return save_path
def download(args,url, save_path, number):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 确保请求成功

        if save_path is None:
            raise ValueError("Save path cannot be None")
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 检查 chunk 是否为空
                    file.write(chunk)
        #print(f"Image downloaded and saved to {save_path}")
        return save_path
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None
def jpg2base64(image_path, return_data_str=True):
    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()
        base64_bytes = base64.b64encode(binary_data)
        base64_string = base64_bytes.decode('utf-8')
    if return_data_str:
        encoded_string = f"data:image/jpeg;base64,{base64_string}"
        return encoded_string
    else:
        return base64_string
def args_into_txt(args,save_path,file_name="args.txt"):
    try:

        with open(os.path.join(save_path,file_name), 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("args\n")
            f.write("=" * 50 + "\n\n")

            args_dict = vars(args)
            for arg_name, arg_value in args_dict.items():
                f.write(f"{arg_name}: {arg_value}\n")
                
            print(f"Args are saved to: {save_path+file_name}")
    except Exception as e:
        print(f"Error saving args to file: {e}")
def image_chuli(args):
    image_files = glob.glob(os.path.join(args.image_dir, "*.*"))
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in image_files if os.path.splitext(f)[1].lower() in valid_extensions]

    if not image_files:
        print(f"No valid images found in {args.image_dir}.")
        exit(1)

    print(f"Found {len(image_files)} images in {args.image_dir}.")
    image_num = len(image_files)
    if args.bingxing:
        #bingxing chuli
        return image_files, image_num
    else:
        
        print("Available images:")
        print(*image_files, sep='\n')
        image_name = input(f"Please enter the image name you want to use (1 to {image_num}): ")
        try:
            image_index = int(image_name) - 1
            if image_index < 0 or image_index >= image_num:
                print(f"Invalid image index: {image_name}")
                if_invalid_input(image_num, image_name)
            args.image_dir = image_files[image_index]
            print(f"Selected image: {args.image_dir}")
            file_name = "original_image.jpg"
            img_save_path = os.path.join(args.save_path, file_name)
            shutil.copy(args.image_dir, img_save_path)
        except ValueError:
            print("Invalid input. Please enter a valid number corresponding to an image.")
            if_invalid_input(image_num, image_name)
def if_invalid_input(image_num, image_name):
    while True: # 持续循环直到获取到有效输入后return
        try:
            image_index = int(image_name) - 1
            if 0 <= image_index < image_num:
                return image_index
            else:
                print(f"Invalid input. Please enter a number between 1 and {image_num}.")
                image_name = input(f"Please enter a valid image name (1 to {image_num}): ")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            image_name = input(f"Please enter a valid image name (1 to {image_num}): ")
def create_result_no_bingxing(args,client):
    if args.bingxing:
        raise ValueError("The bingxing argument is set to True, but use no_bingxing function.")
    prompt = prompt_edit(args)
    print(f"Final prompt: {prompt}")
    image_chuli(args)
    create_result = client.content_generation.tasks.create(
        model = args.model,
        content = [
            {
                "type" : "text",
                "text" : prompt,

            },
            {
                "type" : "image_url",
                "image_url" : {
                    "url" : jpg2base64(args.image_dir)
                },
                "role" : "first_frame"
            }
        ]
    )

    return create_result
def prompt_edit(args):
    prompt = args.prompt
    prompt = prompt[0]
    if args.resolution != "None":
        str_new = "--rs"
        prompt = prompt + " " + str_new + " " + args.resolution
    if args.ratio != "None":
        str_new = "--rt"
        prompt = " ".join([prompt, str_new, f"{args.ratio}"])
    if args.duration != "None":
        str_new = "--dur"
        prompt = " ".join([prompt, str_new, f"{args.duration}"])
    if args.fps != "None":
        str_new = "--fps"
        prompt = " ".join([prompt, str_new, f"{args.fps}"])
    return prompt
def query_result_bingxing(args, task_id, client, outdir, image_path, retry_seconds=3):
    if not args.bingxing:
        raise ValueError("The bingxing argument is set to False, but use bingxing function.")
    while True:
        get_result = client.content_generation.tasks.get(task_id=task_id)
        status = get_result.status
        if status == "succeeded":
            #print(get_result)
            break
        elif status == "failed":
            print("------ Task Failed ------")
            print(f"Error: {get_result.error}")
            break
        else:
            time.sleep(retry_seconds)
    return get_result
def create_result_bingxing(args, client, image_path, i, image_num):
    if not args.bingxing:
        raise ValueError("The bingxing argument is set to False, but use bingxing function.")
    prompt = args.prompt
    dirname = f"{i}_of_{image_num}"
    outdir = os.path.join(args.save_path, dirname)
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    shutil.copy(image_path, outdir)
    create_result = client.content_generation.tasks.create(
        model = args.model,
        content = [
            {
                "type" : "text",
                "text" : prompt,

            },
            {
                "type" : "image_url",
                "image_url" : {
                    "url" : jpg2base64(image_path)
                },
                "role" : "first_frame"
            }
        ]
    )
    result = query_result_bingxing(args, create_result.id, client, outdir, image_path)
    save_path = download_result(args,result,outdir)
    image_from_video(save_path, args.num_of_frames)
    return 
def query_result(args, task_id, client, retry_seconds=3):
    while True:
        get_result = client.content_generation.tasks.get(task_id=task_id)
        status = get_result.status
        if status == "succeeded":
            print("------ Task Succeeded ------")
            #print(get_result)
            break
        elif status == "failed":
            print("------ Task Failed ------")
            print(f"Error: {get_result.error}")
            break
        else:
            print(f"Current status: {status}. Retrying after {retry_seconds} seconds...")
            time.sleep(retry_seconds)
    return get_result
def prompt_read(args):
    if args.prompt == "None":
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f.readlines() if line.strip()]
            args.prompt = prompts
    else:
        args.prompt = [args.prompt]
    return args.prompt