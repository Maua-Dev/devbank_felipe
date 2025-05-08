from enum import Enum
import os

from .errors.environment_errors import EnvironmentNotFound
from .repo.account_repository_interface import IAccountRepository
from .repo.transaction_repository_interface import ITransactionRepository


class STAGE(Enum):
    DOTENV = "DOTENV"
    DEV = "DEV"
    PROD = "PROD"
    TEST = "TEST"


class Environments:
    """
    Defines the environment variables for the application. You should not instantiate this class directly.
    Please use Environments.get_envs() method instead.
    """
    stage: STAGE

    def _configure_local(self):
        from dotenv import load_dotenv
        load_dotenv()
        os.environ["STAGE"] = os.environ.get("STAGE") or STAGE.TEST.value

    def load_envs(self):
        if "STAGE" not in os.environ or os.environ["STAGE"] == STAGE.DOTENV.value:
            self._configure_local()

        self.stage = STAGE[os.environ.get("STAGE")]

    @staticmethod
    def get_account_repo() -> IAccountRepository:
        """
        Returns the appropriate account repository based on the current environment
        """
        if Environments.get_envs().stage == STAGE.TEST:
            from .repo.account_repository_mock import AccountRepositoryMock
            return AccountRepositoryMock()
        else:
            raise EnvironmentNotFound("STAGE")

    @staticmethod
    def get_transaction_repo() -> ITransactionRepository:
        """
        Returns the appropriate transaction repository based on the current environment
        """
        if Environments.get_envs().stage == STAGE.TEST:
            from .repo.transaction_repository_mock import TransactionRepositoryMock
            return TransactionRepositoryMock()
        else:
            raise EnvironmentNotFound("STAGE")

    @staticmethod
    def get_envs() -> "Environments":
        """
        Returns the Environments object. This method should be used to get the Environments object
        instead of instantiating it directly.
        :return: Environments (stage={self.stage})
        """
        envs = Environments()
        envs.load_envs()
        return envs

    def __repr__(self):
        return f"Environments(stage={self.stage})"