# A responsabilidade dele é:
#   Obter os repositórios mais populares e transformá-los em objetos Github_Repository.
#   Ele não deveria saber como fazer HTTP ou GraphQL.

from domain.software_repository import SoftwareRepository, SoftwareRepositoryGateway



class GetPopularRepositories:
    def __init__(self, gateway: SoftwareRepositoryGateway):
        self._gateway = gateway

    def execute(self, quantity: int) -> list[SoftwareRepository]:
        if quantity <= 0:
            raise ValueError("quantity deve ser maior que zero")

        return self._gateway.get_popular(quantity)
