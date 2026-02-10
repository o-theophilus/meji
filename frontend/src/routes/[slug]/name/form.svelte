<script>
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
			window.history.replaceState(history.state, '', `/${resp.item.slug}`);
			module.value.update(resp.item);
			notify.open('Name Saved');
			module.close();
		} else {
			error = resp;
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
