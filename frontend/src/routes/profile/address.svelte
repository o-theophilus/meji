<script>
	import { module, portal } from '$lib/store.js';
	import { token } from '$lib/cookie.js';
	import countries from '$lib/countries.js';

	import Button from '$lib/comp/button.svelte';

	import Info from '$lib/module/info.svelte';
	import Form from '$lib/module/form.svelte';

	let error = {};

	let address = $module.user.address;
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
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/user/${$module.user.key}`, {
			method: 'put',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(address)
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 'good',
				title: '# Details Changed',
				message: `Your address has been changed successfully`,
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
			if (countries[i].name == address.country) {
				states = countries[i].states;
				break;
			}
		}
	}
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Edit Address</div>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="address"> Address: </label>
			<input type="text" bind:value={address.line} id="address" placeholder="Your address here" />
			{#if error.line}
				<p class="error">
					{error.line}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="country"> Country: </label>
			<select
				bind:value={address.country}
				id="country"
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
			{#if error.country}
				<p class="error">
					{error.country}
				</p>
			{/if}
		</div>

		<div class="inputGroup">
			<label for="state"> State: </label>
			<select bind:value={address.state} id="state">
				<option value="" selected default hidden> Select state </option>
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
				bind:value={address.local_area}
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
				bind:value={address.postal_code}
				id="postal_code"
				placeholder="Your postal code here"
			/>
			{#if error.postal_code}
				<p class="error">
					{error.postal_code}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button name="Save" class="primary" />
		</div>
	</form>
</Form>

<style>
</style>
