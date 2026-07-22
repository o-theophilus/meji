<script>
	import { replaceState } from '$app/navigation';
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({ name: module.value.name });
	let error = $state({});

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		} else if (form.name == module.value.name) {
			error.name = 'No changes were made';
		}
		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Saving Item . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/items/${module.value.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			replaceState(`/${result.item.slug}`);
			module.value.update(result.item);
			notify.open('Name Saved');
			module.close();
		} else {
			error = result;
		}
	};
</script>

<Form title="Edit Name" error={error.error}>
	<IG
		name="Name"
		icon="square-pen"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
