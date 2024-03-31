<script>
	import { onMount } from 'svelte';
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

	let form = {
		name: cart.name,
		phone: cart.phone,
		line: cart.line,
		country: cart.country,
		state: cart.state,
		local_area: cart.local_area,
		postal_code: cart.postal_code
	};
	form.country = 'Nigeria';
	form.state = 'Lagos';

	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'This field is required';
		}
		if (!form.phone) {
			error.phone = 'This field is required';
		}
		if (!form.line) {
			error.line = 'This field is required';
		}
		if (!form.country) {
			error.country = 'This field is required';
		}
		if (!form.state) {
			error.state = 'This field is required';
		}
		if (!form.local_area) {
			error.local_area = 'This field is required';
		}
		if (!form.postal_code) {
			error.local_area = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/receiver`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'receiver',
				data: resp.cart
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
			if (countries[i].name == form.country) {
				states = countries[i].states;
				break;
			}
		}
	}

	let { prev } = $module;
	onMount(async () => {
		if (!prev.loaded) {
			let resp = await fetch(`${import.meta.env.VITE_BACKEND}/cart/prev`, {
				method: 'get',
				headers: {
					'Content-Type': 'application/json',
					Authorization: $token
				}
			});
			resp = await resp.json();

			if (resp.status == 200) {
				prev = {
					loaded: true,
					receivers: resp.prev
				};

				$portal = {
					type: 'prev',
					data: prev
				};
			}
		}
	});

	let open = false;
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Receiver's Information</b>
	</svelte:fragment>

	{#if !prev.loaded}
		Loading suggestions . . .
		<br />
		<br />
		<hr />
		<br />
	{:else if prev.receivers.length > 0}
		<div class="title">
			Address suggestion{prev.receivers.length > 1 ? 's' : ''}
			<ButtonFold
				{open}
				on:click={() => {
					open = !open;
				}}
			/>
		</div>
		{#if open}
			<div class="fold" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each prev.receivers as x}
					<Button
						on:click={() => {
							form = {
								name: x.name,
								phone: x.phone,
								line: x.line,
								country: x.country,
								state: x.state,
								local_area: x.local_area,
								postal_code: x.postal_code
							};
						}}
					>
						<p>
							{x.name} | {x.phone} | {x.line}, {x.local_area}, {x.postal_code}, {x.state}
						</p>
					</Button>
				{/each}
			</div>
		{/if}
		<br />
		<hr />
		<br />
	{/if}

	<IG name="name" {error} bind:value={form.name} type="text" placeholder="Name here" />

	<IG name="phone" {error} bind:value={form.phone} type="tel" placeholder="Phone here" />

	<hr />
	<br />

	<IG
		name="line"
		label="address"
		{error}
		bind:value={form.line}
		type="text"
		placeholder="Delivery address here"
	/>

	<IG name="country" {error} let:id>
		<select
			bind:value={form.country}
			{id}
			on:input={() => {
				form.state = '';
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
		<select bind:value={form.state} {id} disabled>
			<option value="" selected disabled hidden> Select state </option>
			{#each states as x}
				<option value={x.name}> {x.name} </option>
			{/each}
		</select>
	</IG>

	<IG
		name="local_area"
		label="Local Government Area"
		{error}
		bind:value={form.local_area}
		type="text"
		placeholder="Your local government area here"
	/>

	<IG
		name="postal_code"
		{error}
		bind:value={form.postal_code}
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
