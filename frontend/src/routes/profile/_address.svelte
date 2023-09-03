<script>
	import { module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import countries from '$lib/countries.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let error = {};

	let address = { ...$module.user.address };
	address.country = address.country ? address.country : 'Nigeria';
	address.state = address.state ? address.state : 'Lagos';

	const validate = async () => {
		error = {};
		if (!address.line) {
			error.line = 'This field is required';
		}
		if (!address.country) {
			error.country = 'This field is required';
		}
		if (!address.state) {
			error.state = 'This field is required';
		}
		if (!address.local_area) {
			error.local_area = 'This field is required';
		}
		if (!address.postal_code) {
			error.postal_code = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = true;
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(address)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = resp.user;
			$module = '';
			$toast = {
				status: '200',
				message: `Address changed`
			};
		} else {
			error = resp;
		}
	};

	let states = [];
	$: {
		for (let i in countries) {
			if (countries[i].name == address.country) {
				states = countries[i].states;
				break;
			}
		}
	}
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Address</b>
	</svelte:fragment>

	<IG name="line" label="Address" {error} let:id>
		<input bind:value={address.line} id="address" type="text" placeholder="Your address here" />
	</IG>

	<IG name="country" {error} let:id>
		<select
			bind:value={address.country}
			{id}
			on:input={() => {
				address.state = '';
			}}
		>
			<option value="" selected default hidden> Select country </option>
			{#each countries as country}
				<option value={country.name}>
					{country.name}
				</option>
			{/each}
		</select>
	</IG>

	<IG name="state" {error} let:id>
		<select bind:value={address.state} {id}>
			<option value="" selected default hidden> Select state </option>
			{#each states as state}
				<option value={state.name}> {state.name} </option>
			{/each}
		</select>
	</IG>

	<IG name="local_area" label="Local Government Area" {error} let:id>
		<input
			type="text"
			bind:value={address.local_area}
			id="local_area"
			placeholder="Your local government area here"
		/>
	</IG>

	<IG name="postal_code" label="Postal Code" {error} let:id>
		<input
			type="text"
			bind:value={address.postal_code}
			id="postal_code"
			placeholder="Your postal code here"
		/>
	</IG>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button name="Save" class="primary" on:click={validate} />
</Form>

<style>
</style>
