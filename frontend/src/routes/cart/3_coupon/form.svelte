<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({ code: '' });
	let error = $state({});

	const validate = () => {
		error = {};

		if (!form.code) {
			error.code = 'This field is required';
		} else if (form.code.length > 100) {
			error.code = 'This field cannot exceed 100 characters';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/receiver`, {
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
			notify.open('Receiver Information Saved');
			module.value.cart = resp.cart;
			module.close();
		} else {
			error = resp;
		}
	};

	const clear = async () => {
		loading.open('Loading . . .');
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/receiver_clear`, {
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
			notify.open('Receiver Information Saved');
			module.value.cart = resp.cart;
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Add Coupon" error={error.error}>
	<IG
		name="Code"
		icon="user"
		error={error.code}
		placeholder="Code here"
		type="text"
		bind:value={form.code}
		required
	/>

	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
