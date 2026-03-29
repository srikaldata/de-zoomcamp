# google cloud platform
* use a service account, generate key and use it for terraform
* or login as follows using the cli and ui in browser:
`gcloud auth application-default login`

* make sure to logout once completed using the folowign two commands
`gcloud auth application-default revoke`
`gcloud auth revoke`

# terraform
* created main.tf and variables.tf
* `terraform fmt` to prettify the .tf files
* make sure to run `terraform destroy` upon completion
