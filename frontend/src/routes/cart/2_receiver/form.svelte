<script>
	import { module, loading, notify, app } from '$lib/store.svelte.js';

	import { IG } from '$lib/input';
	import { Button } from '$lib/button';
	import { Form } from '$lib/layout';

	let form = $state({
		name: module.value.cart.receiver?.name || '',
		phone: module.value.cart.receiver?.phone || '',
		email: module.value.cart.receiver?.email || '',
		address: module.value.cart.receiver?.address?.address || '',
		state: module.value.cart.receiver?.address?.state || '',
		country: module.value.cart.receiver?.address?.country || '',
		postal_code: module.value.cart.receiver?.address?.postal_code || ''
	});

	const validate = () => {
		module.value.error = {};

		form.name = form.name.trim().replace(/\s+/g, ' ');
		if (!form.name) {
			module.value.error.name = 'This field is required';
		} else if (form.name.length > 100) {
			module.value.error.name = 'This field cannot exceed 100 characters';
		}

		form.phone = form.phone.replace(/\s/g, '');
		if (!form.phone) {
			module.value.error.phone = 'This field is required';
		} else if (form.phone.length > 20) {
			module.value.error.phone = 'This field cannot exceed 20 characters';
		}

		form.email = form.email.trim();
		if (!form.email) {
			module.value.error.email = 'This field is required';
		} else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
			module.value.error.email = 'Invalid email address';
		} else if (form.email.length > 255) {
			module.value.error.email = 'This field cannot exceed 255 characters';
		}

		if (!form.address) {
			module.value.error.address = 'This field is required';
		} else if (form.address.length > 255) {
			module.value.error.address = 'This field cannot exceed 255 characters';
		}

		if (!form.state) {
			module.value.error.state = 'This field is required';
		} else if (form.state.length > 20) {
			module.value.error.state = 'This field cannot exceed 20 characters';
		}

		if (!form.country) {
			module.value.error.country = 'This field is required';
		} else if (form.country.length > 20) {
			module.value.error.country = 'This field cannot exceed 20 characters';
		}

		if (form.postal_code && form.postal_code.length > 10) {
			module.value.error.postal_code = 'This field cannot exceed 10 characters';
		}

		Object.keys(module.value.error).length === 0 && submit();
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
			module.value.error = resp;
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
			module.value.error = resp;
		}
	};
</script>

<Form title="Edit Name" error={module.value.error.error}>
	<IG
		name="Name"
		icon="user"
		error={module.value.error.name}
		placeholder="Name here"
		type="text"
		bind:value={form.name}
		required
	/>

	<IG
		name="Phone Number"
		icon="phone"
		error={module.value.error.phone}
		placeholder="Phone number here"
		type="tel"
		bind:value={form.phone}
		required
	/>

	<IG
		name="Email"
		icon="mail"
		error={module.value.error.email}
		placeholder="Email here"
		type="text"
		bind:value={form.email}
		required
	/>

	<IG
		name="Address"
		icon="user"
		error={module.value.error.address}
		placeholder="Address here"
		type="text"
		bind:value={form.address}
		required
	/>

	<IG
		name="State"
		icon="user"
		error={module.value.error.state}
		placeholder="State here"
		type="text"
		bind:value={form.state}
		required
	/>

	<IG
		name="Country"
		icon="user"
		error={module.value.error.country}
		placeholder="Country here"
		type="text"
		bind:value={form.country}
		required
	/>

	<IG
		name="Postal Code"
		icon="user"
		error={module.value.error.postal_code}
		placeholder="Postal Code here"
		type="text"
		bind:value={form.postal_code}
	/>

	<Button
		icon2="x"
		--button-background-color="darkred"
		--button-background-color-hover="red"
		--button-color-hover="white"
		disabled={!module.value.has_receiver()}
		onclick={clear}
	>
		Clear
	</Button>
	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
