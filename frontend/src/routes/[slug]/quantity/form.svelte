<script>
	import { Button } from '$lib/button';
	import { IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify } from '$lib/store.svelte.js';

	let form = $state({
		quantity: module.value.quantity
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (form.quantity && (!Number.isInteger(form.quantity) || form.quantity < 0)) {
			error.quantity = 'Please enter a valid number';
		} else if (form.quantity == module.value.quantity) {
			error.quantity = 'No changes were made';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
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
			notify.open('Quantity Saved');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Quantity" error={error.error}>
	<IG
		name="Quantity"
		error={error.quantity}
		placeholder="Quantity here"
		type="number"
		bind:value={form.quantity}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
