<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({
		price: module.value.price,
		price_old: module.value.price_old
	});
	let error = $state({});

	const validate = () => {
		error = {};

		if (form.price && (!Number.isFinite(form.price) || form.price < 0)) {
			error.price = 'Please enter a valid number';
		} else if (form.price == module.value.price && form.price_old == module.value.price_old) {
			error.price = 'No changes were made';
		}

		if (form.price_old && (!Number.isFinite(form.price_old) || form.price_old < 0)) {
			error.price_old = 'Please enter a valid number';
		} else if (form.price == module.value.price && form.price_old == module.value.price_old) {
			error.price_old = 'No changes were made';
		} else if (form.price_old <= form.price && form.price_old != 0) {
			error.price_old = 'This must be greater than current price';
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
			notify.open('Price Saved');
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Price" error={error.error}>
	<IG
		name="Price (₦)"
		icon="square-pen"
		error={error.price}
		placeholder="Price here"
		type="number"
		bind:value={form.price}
	/>

	<IG
		name="Old Price (₦)"
		icon="square-pen"
		error={error.price_old}
		placeholder="Old Price here"
		type="number"
		bind:value={form.price_old}
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
