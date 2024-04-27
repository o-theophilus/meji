<script>
	import { module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import countries from '$lib/countries.js';

	import Button from '$lib/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let error = {};

	let user = { ...$module.user };
	user.country = user.country ? user.country : 'Nigeria';
	user.state = user.state ? user.state : 'Lagos';

	const validate = async () => {
		error = {};
		if (!user.line) {
			error.line = 'This field is required';
		}
		if (!user.country) {
			error.country = 'This field is required';
		}
		if (!user.state) {
			error.state = 'This field is required';
		}
		if (!user.local_area) {
			error.local_area = 'This field is required';
		}
		if (!user.postal_code) {
			error.postal_code = 'This field is required';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(user)
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$portal = {
				type: 'user',
				data: resp.user
			};
			$module = '';
			$toast = {
				status: 200,
				message: `Address changed`
			};
		} else {
			error = resp;
		}
	};

	let states = [];
	$: {
		for (let i in countries) {
			if (countries[i].name == user.country) {
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

	<IG
		name="line"
		label="Address"
		{error}
		bind:value={user.line}
		type="text"
		placeholder="Your address here"
	/>

	<IG name="country" {error} let:id>
		<select
			bind:value={user.country}
			{id}
			on:input={() => {
				user.state = '';
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
		<select bind:value={user.state} {id}>
			<option value="" selected default hidden> Select state </option>
			{#each states as state}
				<option value={state.name}> {state.name} </option>
			{/each}
		</select>
	</IG>

	<IG
		name="local_area"
		label="Local Government Area"
		{error}
		type="text"
		bind:value={user.local_area}
		placeholder="Your local government area here"
	/>

	<IG
		name="postal_code"
		label="Postal Code"
		{error}
		type="text"
		bind:value={user.postal_code}
		placeholder="Your postal code here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button class="primary" on:click={validate}>Save</Button>
</Form>

<style>
</style>
