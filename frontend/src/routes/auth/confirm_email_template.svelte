<script>
	import { page } from '$app/stores';
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	Thanks for signing up with Meji! Before you start shopping, please confirm your email address by clicking
	the button below:
	<br />
	<br />
	<a
		href="{$page.url.origin}/?module=confirm&token={'{'}token{'}'}"
		style="
	display: block;
	padding: 16px;
	text-decoration: none;
	text-align: center;
	border-radius: 4px;
	border: none;
	color: white;
	background: linear-gradient(0deg, rgb(0, 113, 0) 0%, rgb(0, 177, 0) 100%);"
	>
		<b> Confirm Email Address </b>
	</a>
	<br />
	If the button doesn't work, you can copy and paste the following URL into your web browser:
	<br />
	<br />
	{$page.url.origin}/?module=confirm&token={'{'}token{'}'}
	<br />
	<br />
	Once your email address is confirmed, you'll have full access to Meji's amazing features, including
	a wide selection of products, exclusive deals, and top-notch customer support.
	<br />
	<br />
	If you have any questions, feel free to reach out to our support team at [customer support email].
	<br />
	<br />
	Welcome to Meji! We can't wait to see you shop and enjoy the best experience.
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
