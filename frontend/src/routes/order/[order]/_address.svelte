<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';

	import { tick, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import countries from '$lib/countries.js';

	import HR from '$lib/comp/hr.svelte';
	import Button from '$lib/comp/button.svelte';
	import Button_Fold from '$lib/comp/button_fold.svelte';
	import Form from '$lib/module/form.svelte';

	export let data;
	let { order, previous_recipients } = data;

	let recipient = order.recipient;
	recipient.address.country = 'Nigeria';
	recipient.address.state = 'Lagos';

	let error = {};

	const validate = () => {
		error = {};
		if (!recipient.name) {
			error.name = 'This field is required';
		}
		if (!recipient.phone) {
			error.phone = 'This field is required';
		}
		if (!recipient.address.line) {
			error.address = 'This field is required';
		}
		if (!recipient.address.country) {
			error.country = 'This field is required';
		}
		if (!recipient.address.state) {
			error.state = 'This field is required';
		}
		if (!recipient.address.local_area) {
			error.local_area = 'This field is required';
		}
		if (!recipient.address.postal_code) {
			error.postal_code = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}order/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(recipient)
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				tick(resp.data.order);
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};

	let states = [];
	$: {
		for (let i in countries) {
			if (countries[i].name == order.recipient.address.country) {
				states = countries[i].states;
				break;
			}
		}
	}

	let open = false;
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Delivery Address</div>
	</svelte:fragment>

	{#if order.status == 'pending' && previous_recipients.length > 0}
		<div class="suggestion">
			<div class="title">
				Address suggestion{previous_recipients.length > 1 ? 's' : ''}
				<Button_Fold
					{open}
					on:click={() => {
						open = !open;
					}}
				/>
			</div>
			{#if open}
				<div
					class="body"
					transition:slide|local={{ delay: 0, duration: 200, easing: elasticInOut }}
				>
					{#each previous_recipients as r}
						<Button
							class="wide tiny"
							name="."
							on:click={() => {
								recipient = {
									name: r.name,
									phone: r.phone,
									address: { ...r.address }
								};
							}}
						>
							<p>
								{r.name} | {r.phone}
								<br />
								{r.address.line}, {r.address.local_area}, {r.address.postal_code}, {r.address.state}
							</p>
						</Button>
					{/each}
				</div>
			{/if}
		</div>

		<br />
		<HR />
		<br />
	{/if}

	<form
		on:submit|preventDefault={() => {
			validate();
		}}
		novalidate
		autocomplete="off"
	>
		<div class="inputGroup">
			<label for="name"> Name: </label>
			<input type="text" bind:value={recipient.name} id="name" placeholder="Recepiant name here" />
			{#if error.name}
				<p class="error">
					{error.name}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="phone"> Phone: </label>
			<input
				type="tel"
				bind:value={recipient.phone}
				id="phone"
				placeholder="Recepiant phone here"
			/>
			{#if error.phone}
				<p class="error">
					{error.phone}
				</p>
			{/if}
		</div>

		<HR />

		<div class="inputGroup">
			<label for="address"> Address: </label>
			<input
				type="text"
				bind:value={recipient.address.line}
				id="address"
				placeholder="Delivery address here"
			/>
			{#if error.address}
				<p class="error">
					{error.address}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="country"> Country: </label>
			<select
				bind:value={recipient.address.country}
				id="country"
				on:input={() => {
					recipient.address.state = '';
				}}
				disabled
			>
				<option value="" selected disabled hidden> Select country </option>
				{#each countries as country}
					<option value={country.name}> {country.name} </option>
				{/each}
			</select>
			{#if error.country}
				<p class="error">
					{error.country}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="state"> State: </label>
			<select bind:value={recipient.address.state} id="state" disabled>
				<option value="" selected disabled hidden> Select country </option>
				{#each states as state}
					<option value={state.name}> {state.name} </option>
				{/each}
			</select>
			{#if error.state}
				<p class="error">
					{error.state}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="local_area"> Local Government Area: </label>
			<input
				type="text"
				bind:value={recipient.address.local_area}
				id="local_area"
				placeholder="Your local government area here"
			/>
			{#if error.local_area}
				<p class="error">
					{error.local_area}
				</p>
			{/if}
		</div>
		<div class="inputGroup">
			<label for="postal_code"> Postal Code: </label>
			<input
				type="text"
				bind:value={recipient.address.postal_code}
				id="postal_code"
				placeholder="Your postal code here"
			/>
			{#if error.postal_code}
				<p class="error">
					{error.postal_code}
				</p>
			{/if}
		</div>
		<HR />
		<div class="inputGroup horizontal">
			<Button class="primary" name="Submit" />
		</div>
	</form>
</Form>

<style>
	.suggestion {
		display: flex;
		flex-direction: column;
		gap: var(--gap2);
	}

	.title {
		position: relative;

		display: flex;
		justify-content: space-between;
		align-items: center;

		color: var(--font1);
	}

	.body {
		padding: var(--gap1);
		background-color: var(--background);
	}

	p {
		font-weight: normal;
		font-size: small;
		text-align: left;
	}
</style>
