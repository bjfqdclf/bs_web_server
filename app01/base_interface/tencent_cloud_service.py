import base64

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.iai.v20200303 import iai_client, models
from app01.base_interface.log_server import LogServer
from conf_obtion import sys_config
import json


class TencentCouldService:
    logger = LogServer("人脸识别")
    SecretId = sys_config.SecretId
    SecretKey = sys_config.SecretKey
    GroupId = sys_config.GroupId

    def get_person_info(self, person_id):
        """获取人员信息"""
        try:
            cred = credential.Credential(self.SecretId, self.SecretKey)
            http_profile = HttpProfile()
            http_profile.endpoint = "iai.tencentcloudapi.com"

            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile
            client = iai_client.IaiClient(cred, "ap-shanghai", client_profile)

            req = models.GetPersonBaseInfoRequest()
            params = {
                'PersonId': person_id,
            }
            req.from_json_string(json.dumps(params))

            resp = client.GetPersonBaseInfo(req)
            data = resp.to_json_string()
            self.logger.info(data)
            return data

        except TencentCloudSDKException as err:
            self.logger.error(err)
            if err.code == 'InvalidParameterValue.PersonIdNotExist':
                return False

    def get_person_list(self):
        """获取人员列表"""
        try:
            cred = credential.Credential(self.SecretId, self.SecretKey)
            http_profile = HttpProfile()
            http_profile.endpoint = "iai.tencentcloudapi.com"

            client_profile = ClientProfile()
            client_profile.httpProfile = http_profile
            client = iai_client.IaiClient(cred, "ap-shanghai", client_profile)

            req = models.GetPersonListRequest()
            params = {
                'GroupId': self.GroupId,
            }
            req.from_json_string(json.dumps(params))

            resp = client.GetPersonList(req)
            data = resp.to_json_string()
            self.logger.info(data)
            return data

        except TencentCloudSDKException as err:
            self.logger.error(err)

    def delete_face(self, person_id):
        try:
            cred = credential.Credential(self.SecretId, self.SecretKey)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iai.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile)

            req = models.DeletePersonRequest()
            params = {
                "PersonId": person_id
            }
            req.from_json_string(json.dumps(params))

            resp = client.DeletePerson(req)
            data = resp.to_json_string()
            self.logger.info(data)
            return data

        except TencentCloudSDKException as err:
            self.logger.error(err)

    def add_face(self, params, img_dir):
        try:
            cred = credential.Credential(self.SecretId, self.SecretKey)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "iai.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = iai_client.IaiClient(cred, "ap-shanghai", clientProfile)

            req = models.CreatePersonRequest()
            img_base64 = self.change_base64(img_dir)
            params['Image'] = img_base64
            params['GroupId'] = self.GroupId
            req.from_json_string(json.dumps(params))

            resp = client.CreatePerson(req)
            data = resp.to_json_string()
            self.logger.info(data)
            return data

        except TencentCloudSDKException as err:
            self.logger.error(err)

    @staticmethod
    def change_base64(img_dir, img=None):
        if img_dir:
            with open(img_dir, 'rb') as f:
                base64_data = base64.b64encode(f.read())
                base64_code = base64_data.decode()
        else:
            base64_code = img
        return base64_code

    def check_person_exist(self, person_id):
        """检查人员是否存在"""
        return self.get_person_info(person_id)


tencent_cloud_service = TencentCouldService()
