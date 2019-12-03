import asyncio
import email
import email.header
import json
import os
import miio
import re
from utils import async_helper, logger

DEFAULT_CFG_PATH = 'cfg.json'
log = logger.create_logger(
    os.path.splitext(os.path.basename(__file__))[0]
)


def load_config(config_path=None):
    """Load the configuration from file"""
    if config_path is None:
        config_path = DEFAULT_CFG_PATH
    with open(config_path) as cfg_f:
        cfg_data = json.load(cfg_f)
        return cfg_data


class EmailHandler(object):
    """Email handler"""
    def __init__(self, cfg_path):
        super().__init__()
        self._cfg_data = load_config(cfg_path)
        self._reboot_task = None

    async def handler_RCPT(
            self, server, session, envelope, address, rcpt_options
    ):
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        msg = email.message_from_bytes(envelope.content)
        sub_bytes, encoding = email.header.decode_header(msg['subject'])[0]
        subject = sub_bytes.decode(encoding)
        log.info('Received email with subject: %s', subject)
        asyncio.create_task(self._check_email_subject(subject))
        return '250 Message accepted for delivery'

    async def _check_email_subject(self, subject):
        """Check the email subject"""
        subject_regex = re.compile(self._cfg_data['subject_regex'])
        matched = subject_regex.match(subject)
        if matched and \
           matched.group(1) == self._cfg_data['cam_target']:
            if matched.group(2) == self._cfg_data['cam_offline_indicator']:
                if self._reboot_task is None:
                    self._reboot_task = asyncio.create_task(self._reboot_cam())
                    await self._reboot_task
                    self._reboot_task = None
            elif matched.group(2) == self._cfg_data['cam_online_indicator']:
                if self._reboot_task is not None:
                    self._reboot_task.cancel()
                    self._reboot_task = None

    async def _reboot_cam(self):
        """Reboot the camera"""
        await asyncio.sleep(30)

        log.info("Try to reboot the cam(%s)", self._cfg_data['socket_ip'])
        device = miio.chuangmi_plug.ChuangmiPlug(
            ip=self._cfg_data['socket_ip'], token=self._cfg_data['socket_token']
        )
        result = await async_helper.async_call(device.off)

        log.info('off %s', result)

        await asyncio.sleep(1)

        result = await async_helper.async_call(device.on)
        log.info('on %s', result)


if __name__ == '__main__':
    import argparse
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--config')
    args = arg_parser.parse_args()

    from aiosmtpd.controller import Controller
    controller = Controller(EmailHandler(args.config), hostname='0.0.0.0')
    controller.start()

    asyncio.get_event_loop().run_forever()
