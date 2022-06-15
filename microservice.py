from kubernetes import client, config
from kubernetes.client import configuration
from pick import pick  # install pick using `pip install pick`
from datetime import datetime, timezone, timedelta



time_utc = datetime.now(timezone.utc)
hours_added = timedelta(hours = 2)
time_cet = time_utc + hours_added


def main():
    contexts, active_context = config.list_kube_config_contexts()
    if not contexts:
        print("Cannot find any context in kube-config file.")
        return
    contexts = [context['name'] for context in contexts]
    active_index = contexts.index(active_context['name'])
    option, _ = pick(contexts, title="Pick the context to load",
                     default_index=active_index)

    config.load_kube_config(context=option)

    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for item in ret.items:
        print({"pod": item.metadata.name,
         "rule_evaluation": [{"name": "image_prefix", "valid": ( "bitnami/" in item.spec.containers[0].image)},
          {"name": "team_label_present", "valid": (item.metadata.name[0] in "team") },
           {"name": "recent_start_time", "valid": (time_cet - item.status.start_time).days < 7}]})


if __name__ == '__main__':
    main()
