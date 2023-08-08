<script>
	import { slide } from 'svelte/transition';
	import { elasticInOut } from 'svelte/easing';
	import { portal, module, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import countries from '$lib/countries.js';

	import HR from '$lib/comp/hr.svelte';
	import Button from '$lib/button.svelte';
	import Button_Fold from '$lib/button_fold.svelte';
	import Form from '$lib/module/form.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/module/info.svelte';

	let { order } = $module;
	let { previous_recipients } = $module;

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
			error.line = 'This field is required';
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
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/order/${order.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(recipient)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.order;

			$module = {
				module: Info,
				status: '200',
				title: '# Details Updated',
				message: 'Recipient information has been updated successfully',
				button: [
					{
						name: 'Ok',
						icon: 'ok',
						fn: () => {
							$module = '';
						}
					}
				]
			};
		} else {
			error = resp;
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
		<b>Delivery Address</b>
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

	<IG name="name" {error} let:id>
		<input bind:value={recipient.name} {id} type="text" placeholder="Name here" />
	</IG>

	<IG name="phone" {error} let:id>
		<input bind:value={recipient.phone} {id} type="tel" placeholder="Phone here" />
	</IG>

	<HR />
	<br />

	<IG name="line" label="address" {error} let:id>
		<input
			bind:value={recipient.address.line}
			{id}
			type="text"
			placeholder="Delivery address here"
		/>
	</IG>

	<IG name="country" {error} let:id>
		<select
			bind:value={recipient.address.country}
			{id}
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
	</IG>

	<IG name="state" {error} let:id>
		<select bind:value={recipient.address.state} {id} disabled>
			<option value="" selected disabled hidden> Select country </option>
			{#each states as state}
				<option value={state.name}> {state.name} </option>
			{/each}
		</select>
	</IG>

	<IG name="local_area" label="Local Government Area" {error} let:id>
		<input
			bind:value={recipient.address.local_area}
			{id}
			type="text"
			placeholder="Your local government area here"
		/>
	</IG>

	<IG name="postal_code" {error} let:id>
		<input
			bind:value={recipient.address.postal_code}
			{id}
			type="text"
			placeholder="Your postal code here"
		/>
	</IG>

	<Button name="Submit" class="primary" on:click={validate} />
</Form>

<style>
	.suggestion {
		display: flex;
		flex-direction: column;
		gap: var(--sp2);
	}

	.title {
		position: relative;

		display: flex;
		justify-content: space-between;
		align-items: center;

		color: var(--ac1);
	}

	.body {
		padding: var(--sp1);
		background-color: var(--ac5);
	}

	p {
		font-weight: normal;
		font-size: small;
		text-align: left;
	}
</style>
