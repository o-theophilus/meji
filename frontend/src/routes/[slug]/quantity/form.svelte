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
			module.value.update(result.item);
			notify.open('Quantity Saved');
			module.close();
		} else {
			error = result;
		}
	};
</script>

<Form title="Edit Quantity" error={error.error}>
	<IG
		name="Quantity"
		error={error.quantity}
		placeholder="Quantity here"
		type="quantity"
		bind:value={form.quantity}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
