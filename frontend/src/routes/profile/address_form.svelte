<script>
	import { module, portal, toast, loading } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import countries from '$lib/countries.js';

	import Button from '$lib/button/button.svelte';
	import Form from '$lib/form.svelte';
	import IG from '$lib/input_group.svelte';

	let error = {};
	let form = {
		line: $module.user.line,
		country: $module.user.country,
		state: $module.user.state,
		local_area: $module.user.local_area,
		postal_code: $module.user.postal_code
	};
	form.country = form.country ? form.country : 'Nigeria';
	form.state = form.state ? form.state : 'Lagos';

	const validate = async () => {
		error = {};
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
			error.postal_code = 'This field is required';
		}
		if (
			`${form.line} ${form.country} ${form.state} ${form.local_area} ${form.postal_code}` ==
			`${$module.user.line} ${$module.user.country} ${$module.user.state} ${$module.user.local_area} ${$module.user.postal_code}`
		) {
			error.error = 'no change';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'saving . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
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
			if (countries[i].name == form.country) {
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
		bind:value={form.line}
		type="text"
		placeholder="Your address here"
	/>

	<IG name="country" {error} let:id>
		<select
			bind:value={form.country}
			{id}
			on:input={() => {
				form.state = '';
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
		<select bind:value={form.state} {id}>
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
		bind:value={form.local_area}
		placeholder="Your local government area here"
	/>

	<IG
		name="postal_code"
		label="Postal Code"
		{error}
		type="text"
		bind:value={form.postal_code}
		placeholder="Your postal code here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button primary on:click={validate}>Save</Button>
</Form>

<style>
</style>
