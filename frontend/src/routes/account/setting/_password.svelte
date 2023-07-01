<script>
	import { user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Button from '$lib/comp/button.svelte';

	import Form from '$lib/module/form.svelte';
	import Info from '$lib/module/info.svelte';

	import Email from './_password_email_template.svelte';
	let email;

	let error;

	const submit = async () => {
		let mail_content = email.innerHTML;

		const _resp = await fetch(`${import.meta.env.VITE_BACKEND}password`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify({
				mail_content
			})
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			if (resp.status == 200) {
				$module = {
					module: Info,
					data: {
						status: 'good',
						title: '# Password Recovery Email Sent',
						message: `A password change message has been sent to your email`,
						button: [
							{
								name: 'Ok',
								icon: 'ok'
							}
						]
					}
				};
			} else {
				error = resp.message;
			}
		}
	};
</script>

<Form>
	<svelte:fragment slot="title">Change Password</svelte:fragment>

	<form on:submit|preventDefault={submit} novalidate autocomplete="off">
		<div class="inputGroup horizontal">
			Please press the button to send a password reset link to your email.
		</div>

		<div class="inputGroup horizontal">
			<Button name="Send" class="primary" />
		</div>
		{#if error}
			<div class="inputGroup">
				<p class="error">
					{error}
				</p>
			</div>
		{/if}
	</form>
</Form>

<div bind:this={email} style="display: none;">
	<Email name={$user.name} />
</div>
