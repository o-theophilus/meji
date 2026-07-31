<script>
	import { page } from '$app/state';
	import { Button } from '$lib/button';
	import { Dropdown, IG } from '$lib/input';
	import { Form } from '$lib/layout';
	import { app, loading, module, notify, page_state } from '$lib/store.svelte.js';

	let cart = module.value.ops.cart;
	let form = $state({
		name: cart.receiver?.name || '',
		phone: cart.receiver?.phone || '',
		email: cart.receiver?.email || '',
		address: cart.receiver?.address?.address || '',
		area: cart.receiver?.address?.area || '',
		state: 'Lagos',
		country: 'Nigeria'
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

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		loading.open('Loading . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/cart/receiver`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			notify.open('Receiver Information Saved');
			module.value.ops.cart = result.cart;
			page_state.set_data('cart', result);
			module.close();
		} else {
			error = result;
		}
	};

	const clear = async () => {
		loading.open('Loading . . .');
		let response = await fetch(`${import.meta.env.VITE_BACKEND}/cart/receiver`, {
			method: 'delete',
			headers: {
				'Content-Type': 'application/json',
				Authorization: app.token
			},
			body: JSON.stringify(form)
		});
		let result = await response.json();
		loading.close();

		if (response.status == 200) {
			notify.open('Receiver Information Saved');
			module.value.ops.cart = result.cart;
			page_state.set_data('cart', result);
			module.close();
		} else {
			error = result;
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

	<IG name="Area" error={error.area}>
		{#snippet input()}
			<Dropdown
				--select-color="var(--ft2)"
				--select-color-hover="var(--ft2)"
				--select-background-color="var(--input)"
				--select-background-color-hover="var(--input)"
				--select-outline-color="var(--input)"
				--select-outline-color-hover="var(--ft1)"
				--select-width="calc(100% - 2 * 16px)"
				--select-justify="left"
				--select-gap="16px"
				icon="map-pin"
				list={page.data.areas}
				bind:value={form.area}
			></Dropdown>
		{/snippet}
	</IG>

	<IG
		name="State"
		icon="map-pin"
		error={error.state}
		placeholder="State here"
		type="text"
		bind:value={form.state}
		disabled
	/>

	<IG
		name="Country"
		icon="map-pin"
		error={error.country}
		placeholder="Country here"
		type="text"
		bind:value={form.country}
		disabled
	/>

	<Button
		icon2="x"
		--button-background-color="darkred"
		--button-background-color-hover="red"
		--button-color-hover="white"
		disabled={!module.value.ops.has_receiver}
		onclick={clear}
	>
		Clear
	</Button>
	<Button icon2="send-horizontal" onclick={validate}>Submit</Button>
</Form>
