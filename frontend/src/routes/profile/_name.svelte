<script>
	import { portal, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/button.svelte';
	import Info from '$lib/module/info.svelte';
	import Form from '$lib/module/form.svelte';
	import IG from '$lib/input_group.svelte';

	let error = {};
	let {name} = $module.user;

	const validate = async () => {
		error = {};
		if (!name) {
			error.name = 'This field is required';
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
			body: JSON.stringify({ name })
		});
		resp = await resp.json();

		if (resp.status == 200) {
			$portal = resp.user;

			$module = {
				module: Info,
				status: 200,
				title: '# Details Changed',
				message: `Your name has been changed successfully`,
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
		<b>Edit Name</b>
	</svelte:fragment>

	<IG name="name" {error} let:id>
		<input bind:value={name} {id} type="text" placeholder="Your fullname here" />
	</IG>

	<Button name="Save" class="primary" on:click={validate} />
</Form>

<style>
</style>
