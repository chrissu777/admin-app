from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from .models import Recording
from .serializers import RecordingSerializer
from django.http import StreamingHttpResponse

import boto3
import aws_encryption_sdk
from aws_encryption_sdk import CommitmentPolicy
from aws_encryption_sdk.streaming_client import StreamDecryptor
import aws_encryption_sdk.key_providers.kms
from aws_encryption_sdk.identifiers import CommitmentPolicy
from aws_encryption_sdk.streaming_client import DecryptorConfig, StreamDecryptor
from aws_encryption_sdk.streaming_client import StreamEncryptor
from aws_cryptographic_material_providers.mpl.models import CreateAwsKmsKeyringInput
from aws_cryptographic_material_providers.mpl import AwsCryptographicMaterialProviders
from aws_cryptographic_material_providers.mpl.config import MaterialProvidersConfig
from aws_cryptographic_material_providers.mpl.models import CreateAwsKmsKeyringInput
from aws_cryptographic_material_providers.mpl.references import IKeyring

KMS_KEY_ARN = 'arn:aws:kms:us-east-1:203918845922:key/f0e18996-d4a0-49f6-827d-cc8915c5f864'

from rest_framework.response import Response    
class RecordingViewSet(viewsets.ModelViewSet):
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        recording = self.get_object()
        s3 = boto3.client('s3', region_name='us-east-1')
        s3_obj = s3.get_object(Bucket='weaponwatch-demo', Key=recording.s3_filepath)
        encrypted_stream = s3_obj['Body']
        # Initalize AWS Encryption SDK client with required policy
        client = aws_encryption_sdk.EncryptionSDKClient(
            commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
        )

        # Create KMS client for key decryption
        kms_client = boto3.client('kms', region_name="us-east-1")

        # Configure cryptographic material providers
        mat_prov: AwsCryptographicMaterialProviders = AwsCryptographicMaterialProviders(
            config=MaterialProvidersConfig()
        )

        # Create AWS KMS keyring for decryption
        keyring_input: CreateAwsKmsKeyringInput = CreateAwsKmsKeyringInput(
            kms_key_id=KMS_KEY_ARN,
            kms_client=kms_client
        )
        kms_keyring: IKeyring = mat_prov.create_aws_kms_keyring(
            input=keyring_input
        )
        config = DecryptorConfig(
            keyring=kms_keyring,
            source=encrypted_stream,
            commitment_policy=CommitmentPolicy.REQUIRE_ENCRYPT_REQUIRE_DECRYPT
        )

        decryptor = StreamDecryptor(
            config=config
        )
        response = StreamingHttpResponse(
            decryptor,
            content_type='video/mp4'
        ) 
        response["Content-Disposition"] = f'attachment'
        return response