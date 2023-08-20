<script>
	import { portal, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import IG from '$lib/input_group.svelte';
	import Info from '$lib/info.svelte';
	import Form from '$lib/form.svelte';

	let error = {};
	let { phone } = $module.user;

	const validate = async () => {
		error = {};
		if (!phone) {
			error.phone = 'this field is required';
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
			body: JSON.stringify({ phone })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: `Your phone number has been changed successfully`,
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
</script>

<Form>
	<svelte:fragment slot="title">
		<b>Edit Phone Number</b>
	</svelte:fragment>
	<IG name="phone" {error} let:id>
		<input bind:value={phone} {id} type="tel" placeholder="Your phone here" />
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
