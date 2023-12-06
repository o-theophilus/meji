<script>
	import { slide } from 'svelte/transition';
	import { cubicInOut } from 'svelte/easing';
	import { portal, module, loading, toast } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import countries from '$lib/countries.js';

	import Button from '$lib/button.svelte';
	import ButtonFold from '$lib/button.fold.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let { cart } = $module;
	let { previous_receivers } = $module;

	let receiver = { ...cart.receiver };
	receiver.address.country = 'Nigeria';
	receiver.address.state = 'Lagos';

	let error = {};

	const validate = () => {
		error = {};
		if (!receiver.name) {
			error.name = 'This field is required';
		}
		if (!receiver.phone) {
			error.phone = 'This field is required';
		}
		if (!receiver.address.line) {
			error.line = 'This field is required';
		}
		if (!receiver.address.country) {
			error.country = 'This field is required';
		}
		if (!receiver.address.state) {
			error.state = 'This field is required';
		}
		if (!receiver.address.local_area) {
			error.local_area = 'This field is required';
		}
		if (!receiver.address.postal_code) {
			error.postal_code = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart_receiver`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(receiver)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'receiver',
				data: resp.cart.receiver
			};
			$module = '';
			$toast = {
				status: '200',
				message: "Receiver's information updated"
			};
		} else {
			error = resp;
		}
	};

	let states = [];
	$: {
		for (let i in countries) {
			if (countries[i].name == cart.receiver.address.country) {
				states = countries[i].states;
				break;
			}
		}
	}

	let open = false;
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Receiver's Information</b>
	</svelte:fragment>

	{#if previous_receivers.length > 0}
		<div class="title">
			Address suggestion{previous_receivers.length > 1 ? 's' : ''}
			<ButtonFold
				{open}
				on:click={() => {
					open = !open;
				}}
			/>
		</div>
		{#if open}
			<div class="fold" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each previous_receivers as r}
					<Button
						on:click={() => {
							receiver = {
								name: r.name,
								phone: r.phone,
								address: { ...r.address }
							};
						}}
					>
						<p>
							{r.name} |
							{r.phone} |
							{r.address.line}, {r.address.local_area}, {r.address.postal_code}, {r.address.state}
						</p>
					</Button>
				{/each}
			</div>
		{/if}

		<br />
		<hr />
		<br />
	{/if}

	<IG name="name" {error} bind:value={receiver.name} type="text" placeholder="Name here" />

	<IG name="phone" {error} bind:value={receiver.phone} type="tel" placeholder="Phone here" />

	<hr />
	<br />

	<IG
		name="line"
		label="address"
		{error}
		bind:value={receiver.address.line}
		type="text"
		placeholder="Delivery address here"
	/>

	<IG name="country" {error} let:id>
		<select
			bind:value={receiver.address.country}
			{id}
			on:input={() => {
				receiver.address.state = '';
			}}
			disabled
		>
			<option value="" selected disabled hidden> Select country </option>
			{#each countries as country}
				<option value={country.name}> {country.name} </option>
			{/each}
		</select>
	</IG>

	<IG name="state" {error} let:id>
		<select bind:value={receiver.address.state} {id} disabled>
			<option value="" selected disabled hidden> Select country </option>
			{#each states as state}
				<option value={state.name}> {state.name} </option>
			{/each}
		</select>
	</IG>

	<IG
		name="local_area"
		label="Local Government Area"
		{error}
		bind:value={receiver.address.local_area}
		type="text"
		placeholder="Your local government area here"
	/>

	<IG
		name="postal_code"
		{error}
		bind:value={receiver.address.postal_code}
		type="text"
		placeholder="Your postal code here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Ok</Button>
</Form>

<style>
	.title {
		position: relative;

		display: flex;
		justify-content: space-between;
		align-items: center;

		color: var(--ac1);
	}

	.fold {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);

		padding: var(--sp1) 0;
		background-color: var(--ac6);
	}

	p {
		font-weight: normal;
		font-size: small;
		text-align: left;
	}
</style>
