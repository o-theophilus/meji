<script>
	import { module, loading, notify, app, page_state } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let item = { ...module.value.item };

	let form = $state({
		key: item.key,
		quantity: item.quantity,
		variation: item.variation,
		operation: 'replace'
	});
	let error = $state({});

	const validate = () => {
		module.value.ops.error = {};
		error = {};

		if (form.quantity && (!Number.isInteger(form.quantity) || form.quantity < 1)) {
			error.quantity = 'Please enter a valid number';
		} else if (form.quantity > item.available_quantity) {
			error.quantity = `Only ${item.available_quantity} items available in stock`;
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		app.cart_items = app.cart_items.map((x) => {
			if (x.key == form.key && JSON.stringify(x.variation) == JSON.stringify(form.variation)) {
				return { ...x, quantity: form.quantity };
			}
			return x;
		});

		loading.open('Updating item quantity . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		loading.close();

		if (resp.status == 200) {
			app.cart_items = resp.items;
			notify.open('item quantity updated');
			module.close();
			page_state.clear('cart');
		} else {
			error = resp;
		}
	};
</script>

<Form
	title="Edit Quantity"
	description="Available Quantity ({item.available_quantity})"
	error={error.error}
>
	<IG
		name="Quantity"
		error={error.quantity}
		type="number"
		bind:value={form.quantity}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>

<style>
</style>
