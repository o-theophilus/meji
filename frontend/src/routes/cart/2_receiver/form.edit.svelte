<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let cart = module.value.ops.cart;
	let form = $state({
		name: cart.receiver?.name || '',
		phone: cart.receiver?.phone || '',
		email: cart.receiver?.email || '',
		address: cart.receiver?.address?.address || '',
		state: cart.receiver?.address?.state || '',
		country: cart.receiver?.address?.country || '',
		postal_code: cart.receiver?.address?.postal_code || ''
	});
	let error = $state({});

	const validate = () => {
		module.value.ops.error = {};
		error = {};

		if (form.name) if (form.name) form.name = form.name.trim().replace(/\s+/g, ' ');
		if (!form.name) {
			error.name = 'This field is required';
		} else if (form.name.length > 100) {
			error.name = 'This field cannot exceed 100 characters';
		}

		form.phone = form.phone.replace(/\s/g, '');
		if (!form.phone) {
			error.phone = 'This field is required';
		} else if (form.phone.length > 20) {
			error.phone = 'This field cannot exceed 20 characters';
		}

		if (form.email) if (form.email) form.email = form.email.trim();
		if (!form.email) {
			error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			error.email = 'Invalid email address';
		} else if (form.email.length > 255) {
			error.email = 'This field cannot exceed 255 characters';
		}

		if (!form.address) {
			error.address = 'This field is required';
		} else if (form.address.length > 255) {
			error.address = 'This field cannot exceed 255 characters';
		}

		if (!form.state) {
			error.state = 'This field is required';
		} else if (form.state.length > 20) {
			error.state = 'This field cannot exceed 20 characters';
		}

		if (!form.country) {
			error.country = 'This field is required';
		} else if (form.country.length > 20) {
			error.country = 'This field cannot exceed 20 characters';
		}

		if (form.postal_code && form.postal_code.length > 10) {
			error.postal_code = 'This field cannot exceed 10 characters';
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
			module.value.ops.cart = resp.cart;
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
			module.value.ops.cart = resp.cart;
			module.close();
		} else {
			error = resp;
		}
	};
</script>

<Form title="Edit Name" error={error.error}>
	<IG
		name="Name"
		icon="user"
		error={error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
		required
	/>

	<IG
		name="Phone Number"
		icon="phone"
		error={error.phone}
		placeholder="Phone number here"
		type="tel"
		bind:value={form.phone}
		required
	/>

	<IG
		name="Email"
		icon="mail"
		error={error.email}
		placeholder="Email here"
		type="text"
		bind:value={form.email}
		required
	/>

	<IG
		name="Address"
		icon="map-pin"
		error={error.address}
		placeholder="Address here"
		type="text"
		bind:value={form.address}
		required
	/>

	<IG
		name="State"
		icon="map-pin"
		error={error.state}
		placeholder="State here"
		type="text"
		bind:value={form.state}
		required
	/>

	<IG
		name="Country"
		icon="map-pin"
		error={error.country}
		placeholder="Country here"
		type="text"
		bind:value={form.country}
		required
	/>

	<IG
		name="Postal Code"
		icon="hash"
		error={error.postal_code}
		placeholder="Postal Code here"
		type="text"
		bind:value={form.postal_code}
	/>

	<Button
		icon2="x"
		--button-background-color="darkred"
		--button-background-color-hover="red"
		--button-color-hover="white"
		disabled={!module.value.ops.has_receiver()}
		onclick={clear}
	>
		Clear
	</Button>
	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
