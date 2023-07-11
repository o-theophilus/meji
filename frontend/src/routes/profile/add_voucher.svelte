<script>
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Form from '$lib/module/form.svelte';
	import Button from '$lib/button.svelte';

	let code;
	let error;

	const validate = async () => {
		error = '';

		if (!code) {
			error = 'This field is required';
		} else if (code.length != 10) {
			error = 'invalid code';
		}

		error == '' && submit();
	};

	const submit = async () => {
		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}user_voucher`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({ code })
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$user.acc_balance = resp.data.user.acc_balance;
				$module = '';
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">
		<div class="title">Add Voucher</div>
	</svelte:fragment>

	<svelte:fragment slot="desc">
		<p>Add to your balance.</p>
	</svelte:fragment>

	<form on:submit|preventDefault={validate} novalidate autocomplete="off">
		<div class="inputGroup">
			<label for="voucher"> Voucher Code: </label>
			<input type="voucher" bind:value={code} id="voucher" placeholder="Your code here" />
			{#if error}
				<p class="error">
					{error}
				</p>
			{/if}
		</div>

		<div class="inputGroup horizontal">
			<Button class="primary" name="Add" />
		</div>
	</form>
</Form>
