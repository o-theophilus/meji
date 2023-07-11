<script>
	import { page } from '$app/stores';
	import Template from '$lib/email_template.svelte';
</script>

<Template>
	<b> Hello {'{'}name{'}'}, </b>
	<br />
	<br />
	Thank you for initiating the process to change your password on Meji. To proceed with the password
	change, please click the button below.
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
	{$page.url.origin}/?module=password&token={'{'}token{'}'}
	<br />
	<br />
	If you did not request this action, please disregard this message. The security of your account is
	important to us, and we advise you to contact our customer support immediately if you suspect any unauthorized
	activity.
	<br />
	<br />
	Thank you for being a valued customer. If you have any questions or need further assistance, please
	don't hesitate to reach out to our customer support team.
	<br />
	<br />
	Best regards,
	<br />
	<br />
	<b> Meji </b>
</Template>
