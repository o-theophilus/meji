<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({ information: module.value.information });
	let error = $state({});

	const validate = () => {
		error = {};

		if (form.information == module.value.information) {
			error.information = 'No changes were made';
		} else if (form.information.length > 5000) {
			error.information = 'This field cannot exceed 5000 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		error = {};

		loading.open('Saving Post . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/item/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			module.value.update(resp.item);
			module.close();
			notify.open('Information saved');
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Information" error={error.error}>
	<IG
		name="Information"
		error={error.information}
		type="textarea"
		placeholder="Information here"
		bind:value={form.information}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
