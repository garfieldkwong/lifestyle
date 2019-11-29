import json
import os
import time
import miio
import re
from g_service import gmail
from utils import logger

DEFAULT_CFG_PATH = 'cfg.json'


def load_config(config_path=None):
    """Load the configuration from file"""
    if config_path is None:
        config_path = DEFAULT_CFG_PATH
    with open(config_path) as cfg_f:
        cfg_data = json.load(cfg_f)
        return cfg_data


def run(config=None):
    """Run"""
    log = logger.create_logger(
        os.path.splitext(os.path.basename(__file__))[0]
    )
    cfg_data = load_config(config)
    subject_regex = re.compile(cfg_data['subject_regex'])

    gmail_service = gmail.GMail(
        creds_filename='credentials.json'
    )
    while True:
        log.info('')
        sleep_duration = 60
        msg_infos = gmail_service.list_messages(
            query='is:unread', labelIds=cfg_data['gmail_lable_id']
        )
        for msg_info in msg_infos:
            msg_data = gmail_service.get_message(msg_info['id'])
            subject = ''
            for item in msg_data['payload']['headers']:
                if item['name'] == 'subject':
                    subject = item['value']
            matched = subject_regex.match(subject)
            if matched and \
               matched.group(1) == cfg_data['cam_target'] and \
               matched.group(2) == cfg_data['cam_offline_indicator']:
                device = miio.chuangmi_plug.ChuangmiPlug(
                    ip=cfg_data['socket_ip'], token=cfg_data['socket_token']
                )
                result = device.off()

                log.info('off %s', result)

                time.sleep(1)
                result = device.on()
                log.info('on %s', result)
                sleep_duration = 3600
            gmail_service.mark_as_read(msg_info['id'])
        time.sleep(sleep_duration)


if __name__ == '__main__':
    import argparse
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config')
    args = arg_parser.parse_args()

    run(args.config)