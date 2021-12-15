# CloudOps Technical Exercise: Kubernetes

`main.py` is a simple Python 3 [Bottle](https://bottlepy.org/) web application which uses [Redis](https://redis.io/) as a storage backend. It exposes the following endpoints:

| Endpoint            | HTTP method | Description                                   |
| ------------------- | ----------- | --------------------------------------------- |
| `/hit`              | `POST`      | Increment the count by 1                      |
| `/total`            | `GET`       | Fetch the total `/hit` count                  |
| `/health/liveness`  | `GET`       | Check if the app is running                   |
| `/health/readiness` | `GET`       | Check if the app is ready to service requests |
| `/_metrics`         | `GET`       | Prometheus metrics endpoint                   |

Your task is to write a manifest to deploy this application to Kubernetes - this should take between 30 minutes to 1 hour.

Feel free to edit any files as you see fit.

Your solution should be submitted in the form of a GitHub pull request to this repository.

### Considerations

- Security
- High Availability
- Observability
