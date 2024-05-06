<script>
	import { module, portal, loading, toast, user } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/form.svelte';
	import Button from '$lib/button/button.svelte';
	import IG from '$lib/input_group.svelte';

	let pin;
	let error = {};

	const validate = async () => {
		error = {};

		if (!pin) {
			error.pin = 'This field is required';
		} else if (pin.length != 10) {
			error.pin = 'invalid pin';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		$loading = 'adding . . .';
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/voucher/use`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ pin })
		});
		resp = await resp.json();
		$loading = false;

		if (resp.status == 200) {
			$user = resp.user;

			$module = '';
			$toast = {
				status: 200,
				message: 'voucher added'
			};
		} else {
			error = resp;
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Add Voucher</b>
		Add to your balance.
	</svelte:fragment>

	<IG
		label="voucher pin"
		name="pin"
		{error}
		bind:value={pin}
		type="text"
		placeholder="Your pin here"
	/>

	{#if error.error}
		<p class="error">
			{error.error}
		</p>
		<br />
	{/if}

	<Button primary on:click={validate}>Add</Button>
</Form>
