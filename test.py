from kubernetes import client, config
from kubernetes.client import configuration
from pick import pick  # install pick using `pip install pick`


def main():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])
    option, _ = pick(contexts, title="Pick the context to load",
                     default_index=active_index)
    # Configs can be set in Configuration class directly or using helper
    # utility
    config.load_kube_config(context=option)

    print("Active host is %s" % configuration.Configuration().host)

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items:
        print({"pod": item.metadata.name,
         "rule_evaluation": [{"name": "image_prefix", "valid": "true"},
          {"name": item.metadata.labels, "valid": "true"},
           {"name": item.status.start_time, "valid": "false"}]})


if __name__ == '__main__':
    main()
